from __future__ import annotations
from math import *
from statistics import *
import random
import matplotlib.pyplot as plt


class Hexagon:
    outer_to_inner_factor = sqrt(3) / 2

    @staticmethod
    def area_from_outer(outer_radius: float):
        return Hexagon.area_from_inner(Hexagon.outer_to_inner(outer_radius))

    @staticmethod
    def area_from_inner(inner_radius: float):
        return 2 * sqrt(3) * inner_radius ** 2

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
        return floor(max_value / (self.unit * 1.5))

    def min_x_index(self, min_value):
        return ceil(min_value / (self.unit * 1.5))

    def max_y_index(self, max_value):
        return floor(max_value / (2 * Hexagon.outer_to_inner(self.unit)))

    def min_y_index(self, min_value):
        return ceil(min_value / (2 * Hexagon.outer_to_inner(self.unit)))


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

    def closest_neighbor(self, coordinates):
        distance = float('inf')
        closest = None
        for coordinate in coordinates:
            d = self.distance_to(coordinate)
            if d == 0 or d > distance:
                continue

            closest = coordinate
            distance = d

        return closest

    def print(self):
        print(f"Index ({self.x_index}, {self.y_index}) at ({self.x}, {self.y})")


class RandomSurface:
    def __init__(self, layout: HexagonalGrid):
        self.grid = layout
        self.padding_factor = 3
        self.coordinates_with_padding = list()
        self.coordinates = list()

    def initialize(self, x_max: float, y_max: float, average_distance: float):
        indices = self.get_padded_indices(x_max, y_max, average_distance)
        number_of_coordinates = int(len(indices) * self.probability(average_distance))

        random.shuffle(indices)
        coordinates = list(self.coordinates_from(indices, number_of_coordinates))
        self.coordinates_with_padding, self.coordinates = self.optimize_coordinates(indices, coordinates, x_max, y_max, average_distance)

    def optimize_coordinates(self, indices, coordinates, x_max: float, y_max: float, expected_distance: float):
        while True:
            inner_coordinates = list(self.coordinates_within(coordinates, 0, x_max, 0, y_max))
            if len(inner_coordinates) == 0:
                print("Shuffle coordinates because all were positioned in padding")
                coordinates, indices = self.shuffle_coordinates(indices, coordinates, 0.5)
                continue

            print("requesting average distance for " + str(len(inner_coordinates)) + " inner_coordinates")
            deviation = abs(self.average_distance(inner_coordinates, coordinates) / expected_distance - 1)
            if deviation > 0.05:
                print("Shuffle coordinates due to deviation of " + str(deviation))
                coordinates, indices = self.shuffle_coordinates(indices, coordinates, deviation)
                continue
            break

        print("Optimized coordinates to deviation of " + str(deviation))
        return coordinates, inner_coordinates

    def shuffle_coordinates(self, indices, coordinates, relative_amount):

        random.shuffle(indices)
        count = int(len(coordinates) * relative_amount)
        for _ in range(count):
            coordinates, indices = self.reposition_coordinate(coordinates, indices)

        print("Shuffled " + str(count) + " coordinates")
        return coordinates, indices

    def reposition_coordinate(self, coordinates, indices):
        old = coordinates.pop(0)
        indices.append((old.x_index, old.y_index))
        index = indices.pop(0)
        new = self.grid.get_coordinate(index[0], index[1])
        coordinates.append(new)
        return coordinates, indices

    def coordinates_from(self, indices, count: int):
        for _ in range(count):
            index = indices.pop(0)
            yield self.grid.get_coordinate(index[0], index[1])

    def probability(self, average_distance: float):
        return self.grid.unit_area() / Hexagon.area_from_inner(average_distance)

    def padding_distance(self, average_distance: float):
        return self.padding_factor * average_distance

    def get_padded_indices(self, x_max: float, y_max: float, average_distance: float, x_min: float = 0, y_min:float = 0):
        padding = self.padding_distance(average_distance)
        return self.get_indices(x_min - padding, x_max + padding, y_min - padding, y_max + padding)

    def get_indices(self, x_min: float, x_max: float, y_min: float, y_max: float):
        x_indices = range(self.grid.min_x_index(x_min), self.grid.max_x_index(x_max) + 1)
        y_indices = range(self.grid.min_y_index(y_min), self.grid.max_y_index(y_max) + 1)
        return [(x, y) for x in x_indices for y in y_indices]

    def average_distance_to_closest_neighbor(self):
        return self.average_distance(self.coordinates, self.coordinates_with_padding)

    @staticmethod
    def average_distance(coordinates, neighbors):
        closest_neighbor_distance = list()

        print("calculating average distance for " + str(len(coordinates)) + " coordinates")
        for coordinate in coordinates:
            neighbor = coordinate.closest_neighbor(neighbors)
            closest_neighbor_distance.append(coordinate.distance_to(neighbor))
        return mean(closest_neighbor_distance)

    @staticmethod
    def coordinates_within(coordinates, x_min: float = 0, x_max: float = 0, y_min: float = 0, y_max: float = 0):
        for coordinate in coordinates:
            if coordinate.x < x_min: continue
            if coordinate.x > x_max: continue
            if coordinate.y < y_min: continue
            if coordinate.y > y_max: continue
            yield coordinate


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
        min_distances = list()
        for nano_lever in self.nano_levers:
            position = nano_lever.position
            distances = [position.distance_to(c) for c in self.coordinates]
            distances.remove(0.0)
            minimum = min(distances)
            min_distances.append(minimum)
            print(minimum)
            index = distances.index(minimum)
            result[nano_lever] = self.nano_levers[index]

        print(mean(min_distances))
        return result


if __name__ == '__main__':
    grid = HexagonalGrid(2.5)
    surface = RandomSurface(grid)
    levers = list(surface.nano_levers_for_size(1000, 1000, 60, 16))

    x_values = list(l.position.x for l in levers)
    y_values = list(l.position.y for l in levers)
    plt.plot(x_values, y_values, 'o')
    plt.show()
