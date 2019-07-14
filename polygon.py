from math import *

small_radius = 1.3
side_length = 2 * small_radius
number_of_sides = 4

radius = side_length / (2*(sin(pi / number_of_sides)))

print(radius+small_radius)
print((radius+small_radius)/small_radius)
