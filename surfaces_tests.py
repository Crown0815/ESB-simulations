import unittest
from surfaces import HexagonalGrid, Hexagon, RandomSurface


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
        inners = [1, 2, 5, 10, 20, 50, 100]
        areas = [2.60, 10.39, 64.95, 259.81, 1039.23, 6495.19, 25980.76]

        for inner, area in zip(inners, areas):
            self.assertAlmostEqual(Hexagon.area_from_inner(inner), area, 2)


class RandomSurfaceTests(unittest.TestCase):

    @staticmethod
    def create_test_instance():
        grid = HexagonalGrid(1)
        return RandomSurface(grid)

    def test_positions_for_size(self):
        instance = self.create_test_instance()
        distance = 50

        runs = 10
        while runs > 0:
            positions = list(instance.positions_for_size(2000, 1000, distance))
            print(len(positions))
            self.assertAlmostEqual(instance.average_distance_to_closest_neighbor(positions), distance, delta=distance * 0.1)
            runs -= 1
