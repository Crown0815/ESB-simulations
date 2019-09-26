import unittest
from surfaces import HexagonalGrid, Hexagon, RandomSurface, Coordinate


class HexagonalGridTests(unittest.TestCase):
    @staticmethod
    def create_test_instance(unit: float = 1):
        grid = HexagonalGrid(unit)
        return grid

    def test_distance_to_next_points_is_equal_in_each_direction(self):
        grid = self.create_test_instance()
        zero = grid.get_coordinate(0, 0)
        up = grid.get_coordinate(0, 1)
        right = grid.get_coordinate(1, 0)

        self.assertEqual(zero.x, 0)
        self.assertEqual(zero.y, 0)
        self.assertEqual(up.x, 0)
        self.assertEqual(up.y, 2)
        self.assertEqual(right.x, 1.7320508075688776)
        self.assertEqual(right.y, 1)

        self.assertAlmostEqual(up.distance_to(zero), 2)
        self.assertAlmostEqual(right.distance_to(zero), 2)
        self.assertAlmostEqual(right.distance_to(up), 2)

    def test_unit_area(self):
        grid = self.create_test_instance(2.5)
        self.assertAlmostEqual(grid.unit_area(), 64.95, 2)


class HexagonTests(unittest.TestCase):

    def test_area_from_inner(self):
        outers = [1, 2, 5, 10, 20, 50, 100]
        areas = [2.60, 10.39, 64.95, 259.81, 1039.23, 6495.19, 25980.76]

        for outer, area in zip(outers, areas):
            self.assertAlmostEqual(Hexagon.area_from_outer(outer), area, 2)


class RandomSurfaceTests(unittest.TestCase):

    @staticmethod
    def create_test_instance(grid_distance: int = 5):
        grid = HexagonalGrid(grid_distance)
        return RandomSurface(grid)

    def test_probability(self):
        instance = self.create_test_instance(5)
        self.assertAlmostEqual(instance.probability(5), 1.0, 1)
        self.assertAlmostEqual(instance.probability(10), 0.25, 2)
        self.assertAlmostEqual(instance.probability(15), 0.11, 2)
        self.assertAlmostEqual(instance.probability(20), 0.0625, 4)
        self.assertAlmostEqual(instance.probability(30), 0.02777, 4)
        self.assertAlmostEqual(instance.probability(50), 0.01, 2)
        self.assertAlmostEqual(instance.probability(100), 0.0025, 4)

    def test_distribution_for_different_distances(self):
        self.test_positions_for_size(20)
        self.test_positions_for_size(30)
        self.test_positions_for_size(50)
        self.test_positions_for_size(100)
        self.test_positions_for_size(200)

    def test_positions_for_size(self, distance: int, runs: int = 10):
        instance = self.create_test_instance()
        while runs > 0:
            instance.initialize(500, 500, distance)
            self.assertAlmostEqual(instance.average_distance_to_closest_neighbor(), distance, delta=distance * 0.05)
            runs -= 1

    def test_initialize_coordinates_are_subset_of_padded_coordinates(self):
        instance = self.create_test_instance()
        instance.initialize(1000, 1000, 50)

        self.assertTrue(set(instance.coordinates).issubset(set(instance.coordinates_with_padding)))
        self.assertEqual(len(set(instance.coordinates)), len(instance.coordinates))
        self.assertEqual(len(set(instance.coordinates_with_padding)), len(instance.coordinates_with_padding))


class CoordinateTests(unittest.TestCase):
    @staticmethod
    def create_test_instance(x: float, y: float, x_index: int = 0, y_index: int = 0):
        return Coordinate(x, y, x_index, y_index)

    def test_equality(self):
        instance = self.create_test_instance(1, 1)
        other = self.create_test_instance(1, 1)

        self.assertEqual(instance, other)
