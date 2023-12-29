import unittest

import main1

grid_1 = ['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.']
grid_2 = ['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#']


class Test1(unittest.TestCase):

    def test_get_row_first(self):
        row = main1.get_row(grid_1, 0)
        self.assertEqual('#.##..##.', row)

    def test_get_row_last(self):
        row = main1.get_row(grid_1, 6)
        self.assertEqual('#.#.##.#.', row)

    def test_get_row_out_of_bounds(self):
        row = main1.get_row(grid_1, 7)
        self.assertIsNone(row)

    def test_get_row_negative(self):
        row = main1.get_row(grid_1, -1)
        self.assertIsNone(row)

    def test_get_column_first(self):
        col = main1.get_column(grid_1, 0)
        self.assertEqual("#.##..#", col)

    def test_get_column_last(self):
        col = main1.get_column(grid_1, 8)
        self.assertEqual("..##...", col)

    def test_get_column_out_of_bounds(self):
        col = main1.get_column(grid_1, 9)
        self.assertIsNone(col)

    def test_get_column_negative(self):
        col = main1.get_column(grid_1, -1)
        self.assertIsNone(col)

    def test_find_vertical_reflection(self):
        self.assertEqual(4, main1.find_vertical_reflection(grid_1))

    def test_find_vertical_reflection_none(self):
        self.assertIsNone(main1.find_vertical_reflection(grid_2))

    def test_find_horizontal_reflection(self):
        self.assertEqual(3, main1.find_horizontal_reflection(grid_2))

    def test_find_horizontal_reflection_none(self):
        self.assertIsNone(main1.find_horizontal_reflection(grid_1))
