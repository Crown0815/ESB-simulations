from scipy.constants import *
from math import *


def diffusion_constant_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / radius
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * Boltzmann * temperature * (log(ratio) + correction) / (pi * 4 * length ** 3)


def diffusion_constant_simple_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / (2*radius)
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * Boltzmann * temperature * (log(ratio) + correction) / (pi * 4 * length ** 3)


if __name__ == "__main__":
    small_origami = diffusion_constant_surface_tethered_rod(50e-9, 3.14e-9);
    small_dna = diffusion_constant_surface_tethered_rod(16e-9, 1.3e-9)
    print(small_origami)
    print(small_dna)
    print(small_dna/small_origami)
    print(small_dna/small_origami/5.78*2.96)
