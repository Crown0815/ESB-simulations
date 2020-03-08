from scipy import constants
from math import *
from statistics import mean
from critical_angle_simulation import critical_angle
import numpy as np
import matplotlib.pyplot as plt


# Physical constants
k_B = constants.Boltzmann           # boltzmann constant [J/K]
e = constants.elementary_charge     # elemental charge [C]
epsilon_0 = constants.epsilon_0     # vacuum permitivity [F/m]
N_A = constants.Avogadro            # avogadro constant [1/mol]

# Passivation layer constants
d = 1e-9                            # passivation layer thickness [m] (Langer 2014)
gamma = 0.08                        # factor between electrode potential and effective potential past passivation layer

# Nano-lever constants
xi = 4.2                            # Manning factor to account for charge screening
b = 0.34e-9                         # inter-nucleotide spacing in DNA [m]
r_dna = 1.3e-9                      # radius of DNA cylinder [m]
rho_dna = -2*e/(b*xi)               # effective line charge density in [C/m]
rho_A_dna = -2*e/(b*xi*2*r_dna)     # effective area charge density in [C/m^2]
bp = 48                             # number of nucleotides (defined below as fs)

# 4HB Origami constants
r_4hb = 3.14e-9                     # radius of 4 helix bundle cylinder [m]
rho_4hb = -8*e/(b*xi)               # effective line charge density in [C/m]
rho_A_4hb = rho_4hb/(2*r_4hb)       # effective area charge density in [C/m^2]

# 6HB Origami constants
r_6hb = 3.9e-9                      # radius of 6 helix bundle cylinder [m]
rho_6hb = -12*e/(b*xi)              # effective line charge density in [C/m]
rho_A_6hb = rho_6hb/(2*r_6hb)       # effective area charge density in [C/m^2]

# Protein constants
z = 0                               # real protein charge (defined below zs)
rp = 0e-9                           # protein radius (defined below rps)

# Environment constants
epsilon_r = 78.49                   # relative permitivity of water at 20°C
T = 298.15                          # Temperature [K]
c = 0.05                            # salt concentration in [M]
v = 1                               # salt valency

# Simulation details
angles = [0.01 * constants.pi / 2 * x for x in range(1, 101, 1)]    # angle range
Q = z * e                                                           # total charge of attached molecule


# Base function definitions
def dye_distance_to_surface(angle, length, radius):
    return cos(angle) * radius + sin(angle) * length + d


def dye_fluorescence(surface_distance):
    nanometer_correction = 1e9
    return 0.45 * (1-exp(-0.042 * nanometer_correction * surface_distance)) ** 3.1


def ionic_strength(ion_valency, ion_concentration):
    return ion_valency ** 2 * ion_concentration / 0.1 ** 3          # 0.1 ** 3 is correction from liter to cubic meter


def inverse_debye_length(ion_strength: float, temperature: float, relative_permitivity: float) -> float:
    return sqrt(2 * N_A * e ** 2 / (epsilon_0 * relative_permitivity * k_B * temperature) * ion_strength)


kappa = inverse_debye_length(ionic_strength(v, c), T, epsilon_r)
print(f"Debye length = {1e9/kappa:.2f} nm")


def free_electric_energy_1d(angle, potential, lever_length, lever_radius, line_charge_density):
    return (potential * gamma * line_charge_density / kappa *
            (1 - exp(-kappa * lever_length * sin(angle))) /
            (exp(kappa * lever_radius * cos(angle)) * sin(angle)))


def free_electric_energy_2d(angle, potential, lever_length, lever_radius, area_charge_density):
    return (potential * gamma * area_charge_density / (kappa * kappa) *
            (1 - exp(-kappa * lever_length * sin(angle))) / sin(angle) *
            (1 - exp(-kappa * lever_radius * cos(angle))) / cos(angle))


def orientation_probability(angle, free_electric_energy):
    return cos(angle) * exp(-free_electric_energy / (k_B * T))


def orientation_probability_normalization_factor(probabilities: iter):
    return sum(probabilities)


def orientation_probabilities(angle_critical, free_electric_energy) -> dict:
    probabilities = dict()
    for angle in angles:
        if angle < angle_critical:
            probabilities[angle] = 0
        else:
            probability = orientation_probability(angle, free_electric_energy(angle))
            probabilities[angle] = probability

    normalization_factor = orientation_probability_normalization_factor(probabilities.values())
    normalized_probabilities = dict()
    if normalization_factor == 0:
        return probabilities
    for angle, probability in probabilities.items():
        normalized_probabilities[angle] = probability/normalization_factor

    return normalized_probabilities


def orientation_fluorescence(potential, lever_length, lever_radius, charge_density, angle_critical, free_electric_energy_func) -> float:

    angle_dependent_free_energy = lambda a: free_electric_energy_func(a, potential, lever_length, lever_radius, charge_density)
    probabilities = orientation_probabilities(angle_critical, angle_dependent_free_energy)
    fluorescence = 0
    for angle, probability in probabilities.items():
        fluorescence += probability * dye_fluorescence(dye_distance_to_surface(angle, lever_length, lever_radius))

    return fluorescence


def normalized_fluorescence(potentials, lever_length, lever_radius, charge_density, free_electric_energy_func) -> dict:
    result = dict()
    angle_critical = critical_angle(rp, lever_length, lever_radius)
    print("Critical angle = "+str(angle_critical / pi * 180)+"°")
    for pot in potentials:
        result[pot] = orientation_fluorescence(pot, lever_length, lever_radius, charge_density, angle_critical, free_electric_energy_func)

    fluo_min = min(result.values())
    fluo_max = max(result.values())
    for pot, fluorescence in result.items():
        norm_fluo = (fluorescence - fluo_min) / (fluo_max - fluo_min)
        result[pot] = norm_fluo
    return result


def inflection_point(fluorescence: dict) -> int:
    diff_fluo = np.diff(list(fluorescence.values()))
    return list(fluorescence.keys())[diff_fluo.argmin()]


def inflection_point_slope(fluorescence: dict) -> int:
    diff_fluo = np.diff(list(fluorescence.values()))
    diff_pot = mean(np.diff(list(fluorescence.keys())))
    return diff_fluo.min()/diff_pot


def potential_at_distance(distance: float, start_potential: float) -> float:
    return start_potential * exp(-kappa * distance)


def compare_line_vs_area_charge_density(potentials, length, radius, line_charge_density, area_charge_density):
    area_result = normalized_fluorescence(potentials, length, radius, area_charge_density, free_electric_energy_2d)
    area_fluorescence = list(area_result.values())

    line_result = normalized_fluorescence(_potentials, length, radius, line_charge_density, free_electric_energy_1d)
    line_fluorescence = list(line_result.values())

    print(f'Inflection points for line charge density: {inflection_point(line_result)}, area charge density: {inflection_point(area_result)}')
    print(f'Inflection point slope for line charge density: {inflection_point_slope(line_result)}, area charge density: {inflection_point_slope(area_result)}')

    plt.plot(potentials, line_fluorescence, 'r--', potentials, area_fluorescence)


if __name__ == "__main__":
    _potentials = [-0.2 + 0.005 * x for x in range(0, 121, 1)]  # potential range
    # for potential in potentials:
    #     probabilities = orientation_probabilities(potential, 0, 16e-9, r_dna, rho_dna)
    #     for angle, probability in probabilities.items():
    #         print(f'{potential:.2f}\t\t{angle/pi*180:.2f}\t\t{probability:.8f}\\\\')

    compare_line_vs_area_charge_density(_potentials,  16e-9, r_dna, rho_dna, rho_A_dna)
    compare_line_vs_area_charge_density(_potentials,  32e-9, r_dna, rho_dna, rho_A_dna)
    compare_line_vs_area_charge_density(_potentials,  50e-9, r_4hb, rho_4hb, rho_A_4hb)
    compare_line_vs_area_charge_density(_potentials, 100e-9, r_6hb, rho_6hb, rho_A_6hb)
    plt.show()











