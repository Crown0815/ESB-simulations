from scipy.constants import *
from math import *


def diffusion_constant_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / radius
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * Boltzmann * temperature * (log(ratio) + correction) / (pi * 4 * length ** 3)


def diffusion_constant_relative_term(length, radius):
    ratio = length / radius
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return (log(ratio) + correction) / length ** 3


def diffusion_constant_with_protein_relative_term(length, radius, protein_radius):
    return 1/(6 * protein_radius**3 + 4.5 * protein_radius * (protein_radius + length)**2 +
              1/diffusion_constant_relative_term(length, radius))


def diffusion_constant_temperature_term(temperature=298.15):
    return 3 * Boltzmann * temperature / (pi * 4)


def diffusion_constant_simple_surface_tethered_rod(length, radius, temperature=298.15):
    ratio = length / (2*radius)
    correction = -0.662 + 0.916 / ratio - 0.05 / ratio ** 2
    return 3 * Boltzmann * temperature * (log(ratio) + correction) / (pi * 4 * length ** 3)


if __name__ == "__main__":
    _48mer = diffusion_constant_relative_term(16e-9, 1.3e-9)
    _96mer = diffusion_constant_relative_term(32e-9, 1.3e-9)
    _4hb = diffusion_constant_relative_term(50e-9, 3.14e-9)
    _6hb = diffusion_constant_relative_term(100e-9, 3.9e-9)

    protein_radii = (x/10*1e-9 for x in range(0, 141))
    for r_p in protein_radii:
        print(f"            {r_p*1e9:.1f}       {diffusion_constant_with_protein_relative_term(100e-9, 3.9e-9, r_p)/_6hb:.5f}\\\\")

    small_origami = diffusion_constant_surface_tethered_rod(50e-9, 3.14e-9)
    small_dna = diffusion_constant_surface_tethered_rod(16e-9, 1.3e-9)
    print(small_origami)
    print(small_dna)
    print(small_dna/small_origami)
    print(small_dna/small_origami/5.78*2.96)
