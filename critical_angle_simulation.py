from math import *


def critical_angle(candy_radius, rod_length, rod_radius):
    angle = 0
    old_result = 0
    while angle < pi/2:
        result = critical_angle_equation(candy_radius, rod_length, rod_radius, angle)
        if old_result * result < 0:
            break
        old_result = result
        angle += pi / 100000
    if rod_radius >= candy_radius:
        return 0
    return angle


def critical_angle_degrees(candy_radius, rod_length, rod_radius):
    critical_angle(candy_radius, rod_length, rod_radius) / pi * 180


def critical_angle_equation(candy_radius, rod_length, rod_radius, angle):
    return 1 / 2 * (rod_length + candy_radius) * sin(2 * angle) - candy_radius * cos(angle) + rod_radius * cos(
        angle) ** 2


c = critical_angle(3, 16, 1.3)

rod_l = 50
rod_r = 2.6

candy_radii = range(10, 101, 1)
for candy_r in candy_radii:
    r = candy_r/10.0
    a = critical_angle(r, rod_l, rod_r)
    print(str(r) + " " + str(a)+"\\\\")

