from scipy.constants import *
from math import *


def diffusion_constant_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / radius
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * (log(ratio) + correction) * Boltzmann * temperature / (pi * 4 * length ** 3)


def diffusion_constant_simple_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / (2*radius)
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * (log(ratio) + correction) * Boltzmann * temperature / (pi * 4 * length ** 3)
