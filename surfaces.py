from __future__ import annotations
from math import *
from scipy import constants
from statistics import *
import random
import matplotlib.pyplot as plt
import tikzplotlib


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

    @staticmethod
    def inner_from_area(area: float):
        return sqrt(area /(2 * sqrt(3)))


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

    def probability_of_distance(self, distance):
        respective_unit = Hexagon.inner_to_outer(distance / 2)
        if respective_unit < self.unit:
            raise Exception("distance of {} can not exist on {} grid".format(respective_unit, self.unit))
        return self.unit_area() / Hexagon.area_from_outer(respective_unit)

    def max_x_index(self, max_value):
        return floor(max_value / (self.unit * 1.5))

    def min_x_index(self, min_value):
        return ceil(min_value / (self.unit * 1.5))

    def max_y_index(self, max_value):
        return floor(max_value / (2 * Hexagon.outer_to_inner(self.unit)))

    def min_y_index(self, min_value):
        return ceil(min_value / (2 * Hexagon.outer_to_inner(self.unit)))


class Coordinate:
    def __init__(self, x: float, y: float, x_index: int = 0, y_index: int = 0):
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
        closest_distance = float('inf')
        closest = None
        for coordinate in coordinates:
            distance = self.distance_to(coordinate)
            if distance == 0 or distance > closest_distance:
                continue

            closest = coordinate
            closest_distance = distance

        return closest

    def closer_than(self, distance: float, coordinates):
        for coordinate in coordinates:
            distance_to = self.distance_to(coordinate)
            if distance_to == 0: continue
            if distance_to >= distance: continue
            yield coordinate

    def distances_within(self, distance: float, coordinates):
        for coordinate in coordinates:
            distance_to = self.distance_to(coordinate)
            if distance_to == 0: continue
            if distance_to >= distance: continue
            yield distance_to

    def print(self):
        print(f"Index ({self.x_index}, {self.y_index}) at ({self.x}, {self.y})")

    def __eq__(self, other):
        if other is None: return False
        if self.x != other.x: return False
        if self.y != other.y: return False
        if self.x_index != other.x_index: return False
        if self.y_index != other.y_index: return False
        return True

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.x_index) ^ hash(self.y_index)


class RandomSurface:
    def __init__(self, layout: HexagonalGrid, padding_factor: int = 3):
        self.grid = layout
        self.padding_factor = padding_factor
        self.coordinates_with_padding = list()
        self.padding = list()
        self.coordinates = list()
        self.x_length = 0
        self.y_length = 0
        self.target_distance = 0

    def initialize(self, x_max: float, y_max: float, average_distance: float, verbose=True):
        coordinates, indices = self.distribute_targets(x_max, y_max,
                                                       self.padding_distance(average_distance),
                                                       self.probability(average_distance))

        self.target_distance = average_distance
        self.coordinates_with_padding, self.coordinates, self.padding = \
            self.optimize_coordinates(indices, coordinates, x_max, y_max, average_distance, verbose)

    def distribute_targets(self, x_length: float, y_length: float, padding: float, probability_of_occupation: float):
        self.x_length = x_length
        self.y_length = y_length
        indices = self.indices_with_padding(x_length, y_length, padding)
        number_of_coordinates = int(len(indices) * probability_of_occupation)

        random.shuffle(indices)
        return list(self.coordinates_from(indices, number_of_coordinates)), indices

    def distribute_targets_from_liquid_drop(self, area: float, total_surface_area: float, drop_volume: float, drop_concentration: float, target_immobilization_probability: float):
        number_of_targets = drop_concentration * drop_volume * constants.Avogadro * target_immobilization_probability
        return self.distribute_number_of_targets(area, number_of_targets, total_surface_area)

    def distribute_number_of_targets(self, area: float, number_of_targets: int, total_surface_area: float = None):
        if total_surface_area is None:
            total_surface_area = area
        side_length = sqrt(area)
        available_spots = total_surface_area / self.grid.unit_area()
        probability_of_occupation = number_of_targets / available_spots
        if probability_of_occupation > 1:
            raise Exception(f"Probability is too high: {probability_of_occupation}")
        coordinates, _ = self.distribute_targets(side_length, side_length, 0, probability_of_occupation)
        self.target_distance = None
        self.coordinates_with_padding, self.coordinates, self.padding = \
            self.separate_coordinates(coordinates, side_length, side_length)

    def separate_coordinates(self, coordinates, x_max: float, y_max: float):
        inner_coordinates = list(self.coordinates_within(coordinates, 0, x_max, 0, y_max))
        padding = list(c for c in coordinates if c not in inner_coordinates)
        return coordinates, inner_coordinates, padding

    def optimize_coordinates(self, indices, coordinates, x_max: float, y_max: float, expected_distance: float, verbose=True):
        while True:
            inner_coordinates = list(self.coordinates_within(coordinates, 0, x_max, 0, y_max))
            if len(inner_coordinates) == 0:
                if verbose: print("Shuffle coordinates because all were positioned in padding")
                coordinates, indices = self.shuffle_coordinates(indices, coordinates, 0.5, verbose)
                continue

            if verbose: print("requesting average distance for " + str(len(inner_coordinates)) + " inner_coordinates")
            average_distance = self.average_distance_within(self.max_neighbor_distance(), inner_coordinates,
                                                            coordinates)
            deviation = abs(average_distance / expected_distance - 1)
            if deviation > 0.05:
                if verbose: print("Shuffle coordinates due to deviation of {:.1%} ({}/{})".format(deviation, average_distance,
                                                                                      expected_distance))
                coordinates, indices = self.shuffle_coordinates(indices, coordinates, deviation)
                continue
            break

        if verbose: print("Optimized coordinates to deviation of " + str(deviation))
        padding = list(c for c in coordinates if c not in inner_coordinates)
        return coordinates, inner_coordinates, padding

    def shuffle_coordinates(self, indices, coordinates, relative_amount, verbose=True):

        random.shuffle(indices)
        count = int(len(coordinates) * relative_amount)
        for _ in range(count):
            coordinates, indices = self.reposition_coordinate(coordinates, indices)

        if verbose: print("Shuffled " + str(count) + " coordinates")
        return coordinates, indices

    def max_neighbor_distance(self):
        if self.target_distance is None:
            return inf
        return 1.5 * self.target_distance

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
        return self.grid.probability_of_distance(average_distance)

    def padding_distance(self, average_distance: float):
        return self.padding_factor * average_distance

    def padded_indices(self, x_max: float, y_max: float, average_distance: float, x_min: float = 0, y_min: float = 0):
        padding = self.padding_distance(average_distance)
        return self.indices_with_padding(x_max, y_max, padding, x_min, y_min)

    def indices_with_padding(self, x_max: float, y_max: float, padding: float, x_min: float = 0, y_min: float = 0):
        return self.indices_within(x_min - padding, x_max + padding, y_min - padding, y_max + padding)

    def indices_within(self, x_min: float, x_max: float, y_min: float, y_max: float):
        x_indices = range(self.grid.min_x_index(x_min), self.grid.max_x_index(x_max) + 1)
        y_indices = range(self.grid.min_y_index(y_min), self.grid.max_y_index(y_max) + 1)
        return [(x, y) for x in x_indices for y in y_indices]

    def distance_to_closest_neighbor_average(self):
        return self.distance_average(self.coordinates, self.coordinates_with_padding)

    def distance_to_closest_neighbor_stddev(self):
        return self.distance_stddev(self.coordinates, self.coordinates_with_padding)

    def distances_to_closest_neighbor(self):
        return self.closest_neighbor_distances(self.coordinates, self.coordinates_with_padding)

    def average_distance_to_neighbors(self):
        return self.average_distance_within(self.max_neighbor_distance(), self.coordinates,
                                            self.coordinates_with_padding)

    def visualization(self, figure_size=5):
        f, ax = plt.subplots(figsize=(figure_size, figure_size))
        ax.plot([0, 0, self.x_length, self.x_length, 0], [0, self.y_length, self.y_length, 0, 0], linestyle=":",
                color="#BEBEBE")

        ax.plot(self.x_of(self.coordinates), self.y_of(self.coordinates), 'o', color="black")
        ax.plot(self.x_of(self.padding), self.y_of(self.padding), 'x', color="#BEBEBE")
        return f, ax

    @staticmethod
    def x_of(coordinates):
        return list(c.x for c in coordinates)

    @staticmethod
    def y_of(coordinates):
        return list(c.y for c in coordinates)

    @staticmethod
    def distance_average(coordinates, neighbors):
        return mean(RandomSurface.closest_neighbor_distances(coordinates, neighbors))

    @staticmethod
    def distance_stddev(coordinates, neighbors):
        return stdev(RandomSurface.closest_neighbor_distances(coordinates, neighbors))

    @staticmethod
    def closest_neighbor_distances(coordinates, neighbors):
        closest_neighbor_distance = list()

        for coordinate in coordinates:
            neighbor = coordinate.closest_neighbor(neighbors)
            closest_neighbor_distance.append(coordinate.distance_to(neighbor))
        return closest_neighbor_distance

    @staticmethod
    def average_distance_within(within, coordinates, neighbors):
        closest_neighbor_distance = list()
        for coordinate in coordinates:
            closest_neighbor_distance = closest_neighbor_distance + list(coordinate.distances_within(within, neighbors))
        return mean(closest_neighbor_distance)

    @staticmethod
    def coordinates_within(coordinates, x_min: float = 0, x_max: float = 0, y_min: float = 0, y_max: float = 0):
        for coordinate in coordinates:
            if coordinate.x < x_min: continue
            if coordinate.x > x_max: continue
            if coordinate.y < y_min: continue
            if coordinate.y > y_max: continue
            yield coordinate


def create_surface(grid_size, width, height, distance, figure_size, show_plot=False):
    grid = HexagonalGrid(grid_size)
    surface = RandomSurface(grid)
    surface.initialize(width, height, distance)
    surface.visualization(figure_size)

    tikzplotlib.save("./generated/surface_g{}_d{}_x{}_y{}_f{}.tex".format(grid_size, distance, width, height, figure_size))
    if show_plot: plt.show()


def create_surface_from_drop(grid_size, simulation_area, total_area, volume, concentration, immobilization_probability, figure_size, show_plot=False):
    grid = HexagonalGrid(grid_size)
    surface = RandomSurface(grid)
    surface.distribute_targets_from_liquid_drop(simulation_area, total_area, volume, concentration, immobilization_probability)
    surface.visualization(figure_size)

    tikzplotlib.save("./generated/surface_from_drop_g{}_sa{}_ta{}_v{}_c{}_p{}_f{}.tex".format(grid_size, simulation_area, total_area, volume, concentration, immobilization_probability, figure_size))
    if show_plot: plt.show()


if __name__ == '__main__':
    create_surface(40.5, 1000, 1000, 81, 5)
    # create_surface_from_drop(2.5e-9, 500e-9**2, 2*pi*65e-6**2, 1e-9, 1e-7 * 1.000, 1, 5, True)
    # create_surface_from_drop(2.5e-9, 500e-9**2, 2*pi*65e-6**2, 1e-9, 1e-7 * 0.500, 1, 5, True)
    # create_surface_from_drop(2.5e-9, 500e-9**2, 2*pi*65e-6**2, 1e-9, 1e-7 * 0.250, 1, 5, True)
    # create_surface_from_drop(2.5e-9, 500e-9**2, 2*pi*65e-6**2, 1e-9, 1e-7 * 0.125, 1, 5, True)
