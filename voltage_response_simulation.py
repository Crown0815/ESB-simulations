from scipy import constants
from math import *
from critical_angle_simulation import critical_angle
import matplotlib.pyplot as plt
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
R_dna = 1.3e-9                          # radius of DNA cylinder [m]
rho_eff = -2*e/(b*4.2)               # effective line charge density in [C/m]
bp = 48                             # number of nucleotides (defined below as fs)
L = b * bp                          # nano-lever length
R = R_dna                           # nano-lever radius

# Protein constants
z = 0                               # real protein charge (defined below zs)
rp = 0e-9                           # protein radius (defined below rps)

# Environment constants
epsilon_r = 78.49                   # relative permitivity of water at 20°C
T = 298.15                          # Temperature [K]
c = 0.04                            # salt concentration in [M]
v = 1                               # salt valency

# Simulation details
angles = [0.01 * constants.pi / 2 * x for x in range(1, 101, 1)]     # angle range


# Base function definitions
def molecule_charge(number_of_charges):
    return number_of_charges * e


def dye_distance_to_surface(angle, length, radius):
    return cos(angle) * 2 * radius + sin(angle) * length


def dye_fluorescence(surface_distance):
    nanometer_correction = 1e9
    return 0.45 * (1-exp(-0.042 * nanometer_correction * surface_distance)) ** 3.1


def ionic_strength(ion_valency, ion_concentration):
    return ion_valency ** 2 * ion_concentration / 0.1 ** 3          # 0.1 ** 3 is correction from liter to cubic meter


def inverse_debye_length(ion_strength: float, temperature: float, relative_permitivity: float) -> object:
    return sqrt(2 * N_A * e ** 2 / (epsilon_0 * relative_permitivity * k_B * temperature) * ion_strength)


# Simulation constants
Q = molecule_charge(z)                  # total charge of attached molecule
angle_critical = critical_angle(rp, L, R)
kappa = inverse_debye_length(ionic_strength(v, c), T, epsilon_r)
print("Critical angle = "+str(angle_critical / pi * 180)+"°")
print("Debye length = "+str(1/kappa)+"m")



def orientation_probability(angle, potential):
    return cos(angle) * exp(- potential * gamma * rho_eff / (kappa * k_B * T) * (1 - exp(-kappa * L * sin(angle))) /
                            (exp(kappa * R * cos(angle)) * sin(angle)))


def orientation_probability_molecule_charge_influence(total_charge, angle, potential):
    if molecule_charge == 0:
        return 0
    return total_charge * gamma * potential * rho_eff * b / (k_B * T) / (rho_eff * b) * exp(
            -kappa * ((L + rp) * sin(angle) + R * cos(angle)))


def orientation_probability_normalization_factor(probabilities: iter):
    return sum(probabilities)


def orientation_probabilities(potential) -> dict:
    probabilities = dict()
    for angle in angles:
        if angle < angle_critical:
            probabilities[angle] = 0
        else:
            probability = orientation_probability(angle, potential)
            probabilities[angle] = probability

    normalization_factor = orientation_probability_normalization_factor(probabilities.values())
    normalized_probabilities = dict()
    if normalization_factor == 0:
        return probabilities
    for angle, probability in probabilities.items():
        normalized_probabilities[angle] = probability/normalization_factor

    return normalized_probabilities


def orientation_fluorescence(potential) -> float:
    probabilities = orientation_probabilities(potential)
    fluorescence = 0
    for angle, probability in probabilities.items():
        fluorescence += probability * dye_fluorescence(dye_distance_to_surface(angle, L, R))

    return fluorescence


def normalized_fluorescence(potentials) -> dict:
    result = dict()
    for pot in potentials:
        result[pot] = orientation_fluorescence(pot)

    fluo_min = min(result.values())
    fluo_max = max(result.values())
    for pot, fluorescence in result.items():
        norm_fluo = (fluorescence - fluo_min) / (fluo_max - fluo_min)
        result[pot] = norm_fluo
    return result


potentials = [-0.4 + 0.01 * x for x in range(1, 96, 1)]               # potential range

fluo = normalized_fluorescence(potentials)

diff_fluo = np.diff(list(fluo.values()))
min = diff_fluo.argmin()


plt.plot(list(fluo.keys()), list(fluo.values()), list(fluo.keys())[min], list(fluo.values())[min], 'o')
#plt.show()
print(fluo)

for pot, fl in fluo.items():
    print(str(pot) + " " + str(fl)+"\\\\")














