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
    return critical_angle(candy_radius, rod_length, rod_radius) / pi * 180


def critical_angle_equation(candy_radius, rod_length, rod_radius, angle):
    return 1 / 2 * (rod_length + candy_radius) * sin(2 * angle) - candy_radius * cos(angle) + rod_radius * cos(
        angle) ** 2


if __name__ == "__main__":
    for radius in range(10, 101, 1):
        print(str(radius/10) + "  " + str(critical_angle_degrees(radius/10, 100, 3.9)) + "\\\\")


