import unittest
from surfaces import HexagonalGrid

class HexagonalGridTests(unittest.TestCase):
    @staticmethod
    def create_test_instance():
        grid = HexagonalGrid(1)
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
