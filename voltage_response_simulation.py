from scipy import constants
from math import *
from critical_angle_simulation import critical_angle
import numpy as np

# Physical constants
k_B = constants.Boltzmann           # boltzmann constant [J/K]
e = constants.elementary_charge     # elemental charge [C]
epsilon_0 = constants.epsilon_0     # vacuum permitivity [F/m]
N_A = constants.Avogadro            # avogadro constant [1/mol]

# Passivation layer constants
d = 1e-9                            # passivation layer thickness [m] (Langer 2014)
gamma = 0.08                        # factor between electrode potential and effective potential past passivation layer

# Nano-lever constants
b = 0.34e-9                         # inter-nucleotide spacing in DNA [m]
r_dna = 1.3e-9                      # radius of DNA cylinder [m]
rho_dna = -2*e/(b*4.2)              # effective line charge density in [C/m]
bp = 48                             # number of nucleotides (defined below as fs)

# Protein constants
z = 0                               # real protein charge (defined below zs)
rp = 0e-9                           # protein radius (defined below rps)

# Environment constants
epsilon_r = 78.49                   # relative permitivity of water at 20°C
T = 298.15                          # Temperature [K]
c = 0.06                            # salt concentration in [M]
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


def inverse_debye_length(ion_strength: float, temperature: float, relative_permitivity: float) -> object:
    return sqrt(2 * N_A * e ** 2 / (epsilon_0 * relative_permitivity * k_B * temperature) * ion_strength)


kappa = inverse_debye_length(ionic_strength(v, c), T, epsilon_r)
print("Debye length = "+str(1/kappa)+"m")


def orientation_probability(angle, potential, lever_length, lever_radius, line_charge_density):
    return cos(angle) * exp(- potential * gamma * line_charge_density / (kappa * k_B * T) * (1 - exp(
                            -kappa * lever_length * sin(angle))) /
                            (exp(kappa * lever_radius * cos(angle)) * sin(angle)))


def orientation_probability_normalization_factor(probabilities: iter):
    return sum(probabilities)


def orientation_probabilities(potential, angle_critical, lever_length, lever_radius, line_charge_density) -> dict:
    probabilities = dict()
    for angle in angles:
        if angle < angle_critical:
            probabilities[angle] = 0
        else:
            probability = orientation_probability(angle, potential, lever_length, lever_radius, line_charge_density)
            probabilities[angle] = probability

    normalization_factor = orientation_probability_normalization_factor(probabilities.values())
    normalized_probabilities = dict()
    if normalization_factor == 0:
        return probabilities
    for angle, probability in probabilities.items():
        normalized_probabilities[angle] = probability/normalization_factor

    return normalized_probabilities


def orientation_fluorescence(potential, lever_length, lever_radius, line_charge_density, angle_critical) -> float:

    probabilities = orientation_probabilities(potential, angle_critical, lever_length, lever_radius, line_charge_density)
    fluorescence = 0
    for angle, probability in probabilities.items():
        fluorescence += probability * dye_fluorescence(dye_distance_to_surface(angle, lever_length, lever_radius))

    return fluorescence


def normalized_fluorescence(potentials, lever_length, lever_radius, line_charge_density) -> dict:
    result = dict()
    angle_critical = critical_angle(rp, lever_length, lever_radius)
    print("Critical angle = "+str(angle_critical / pi * 180)+"°")
    for pot in potentials:
        result[pot] = orientation_fluorescence(pot, lever_length, lever_radius, line_charge_density, angle_critical)

    fluo_min = min(result.values())
    fluo_max = max(result.values())
    for pot, fluorescence in result.items():
        norm_fluo = (fluorescence - fluo_min) / (fluo_max - fluo_min)
        result[pot] = norm_fluo
    return result


def inflection_point(fluorescence: dict) -> int:
    diff_fluo = np.diff(list(fluorescence.values()))
    return diff_fluo.argmin()


def inflection_point_slope(fluorescence: dict) -> int:
    diff_fluo = np.diff(list(fluorescence.values()))
    return diff_fluo.min()












