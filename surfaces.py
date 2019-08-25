from __future__ import annotations
from math import *
from statistics import *
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial as sp


class Hexagon:
    outer_to_inner_factor = sqrt(3) / 2

    @staticmethod
    def area_from_outer(outer_radius: float):
        return 3 * sqrt(3) / 2 * outer_radius ** 2

    @staticmethod
    def area_from_inner(inner_radius: float):
        return Hexagon.area_from_outer(inner_radius / Hexagon.outer_to_inner_factor)

    @staticmethod
    def outer_to_inner(outer_hexagon_radius):
        return outer_hexagon_radius * Hexagon.outer_to_inner_factor

    @staticmethod
    def inner_to_outer(inner_hexagon_radius: float):
        return inner_hexagon_radius / Hexagon.outer_to_inner_factor


class HexagonalGrid:

    def __init__(self, inner_hexagon_radius: float = 1):
        self.unit = Hexagon.inner_to_outer(inner_hexagon_radius)

    def get_coordinate(self, x_index: int = 0, y_index: int = 0):
        return Coordinate(self.get_x(x_index), self.get_y(y_index, x_index), x_index, y_index)

    def get_x(self, x_index):
        return x_index * self.unit * 1.5

    def get_y(self, y_index: int = 0, x_index: int = 0):
        offset = 0 if x_index % 2 == 0 else 1
        return (offset + 2 * y_index) * Hexagon.outer_to_inner(self.unit)

    def unit_area(self):
        return Hexagon.area_from_outer(self.unit)

    def max_x_index(self, max_value):
        return floor(max_value / self.unit * 1.5)

    def max_y_index(self, max_value):
        return floor(max_value / (2 * Hexagon.outer_to_inner(self.unit)))


class Coordinate:
    def __init__(self, x: float, y: float, x_index: int, y_index: int):
        self.x = x
        self.y = y
        self.x_index = x_index
        self.y_index = y_index

    def distance_to(self, other: Coordinate) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    @staticmethod
    def default():
        return Coordinate(0, 0, 0, 0)

    def print(self):
        print(f"Index ({self.x_index}, {self.y_index}) at ({self.x}, {self.y})")


class RandomSurface:
    def __init__(self, layout: HexagonalGrid):
        self.grid = layout

    def create_for_size(self, x_max: float, y_max: float, average_distance: float, lever_length: float = 16e-9):

        probability = self.grid.unit_area() / Hexagon.area_from_inner(average_distance / 2)
        levers = list()
        for index in self.get_indices(x_max, y_max):
            if random.random() > probability:
                continue
            coordinate = self.grid.get_coordinate(index[0], index[1])
            levers.append(NanoLever(coordinate, lever_length))
        return levers

    def get_indices(self, x_max: float, y_max: float):
        x_indices = range(self.grid.max_x_index(x_max) + 1)
        y_indices = range(self.grid.max_y_index(y_max) + 1)
        return [(x, y) for x in x_indices for y in y_indices]


class NanoLever:
    def __init__(self, position: Coordinate = Coordinate.default(), length: float = 16e-9):
        self.length = length
        self.position = position


class InterLinker:
    def __init__(self, nano_levers):
        self.nano_levers = nano_levers
        self.coordinates = [l.position for l in self.nano_levers]
        self.nearest_neighbors = self.analyze_nearest_neighbors()

    def analyze_nearest_neighbors(self):
        result = dict()
        for nano_lever in self.nano_levers:
            position = nano_lever.position
            distances = [position.distance_to(c) for c in self.coordinates]
            distances.remove(0.0)
            minimum = min(distances)
            index = distances.index(minimum)
            result[nano_lever] = self.nano_levers[index]

        return result


if __name__ == '__main__':
    grid = HexagonalGrid()
    surface = RandomSurface(grid)
    levers = surface.create_for_size(1000, 1000, 50, 16)
    linker = InterLinker(levers)

    pairs = linker.nearest_neighbors
    distances = [source.position.distance_to(pairs[source].position) for source in pairs]
    print(f"average distance = {mean(distances)}")

    print(linker.nearest_neighbors)

    x_values = list(l.position.x for l in levers)
    y_values = list(l.position.y for l in levers)
    plt.plot(x_values, y_values, 'o')
    # plt.show()