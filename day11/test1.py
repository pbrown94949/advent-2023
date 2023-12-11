import unittest

import main1


class Test1(unittest.TestCase):

    def test_manhattan_distance(self):
        a, b = (7, 2), (12, 6)
        x = main1.calculate_manhattan_distance(a, b)
        self.assertEqual(9, x)
        a, b = (1, 5), (11, 10)
        x = main1.calculate_manhattan_distance(a, b)
        self.assertEqual(15, x)
        a, b = (3, 1), (8, 13)
        x = main1.calculate_manhattan_distance(a, b)
        self.assertEqual(17, x)
        a, b = (12, 1), (12, 6)
        x = main1.calculate_manhattan_distance(a, b)
        self.assertEqual(5, x)

    def get_missing_values(self):
        s = set(3, 7)
        x = main1.get_missing_values(s)
        self.assertEqual(set(1, 2, 4, 5, 6), x)

    def test_get_expanding_rows(self):
        galaxies = set([(1, 1), (3, 1), (9, 1)])
        x = main1.get_expanding_rows(galaxies)
        self.assertEqual(set([0, 2, 4, 5, 6, 7, 8]), x)

    def test_get_expanding_columns(self):
        galaxies = set([(1, 2), (3, 1), (9, 4)])
        x = main1.get_expanding_columns(galaxies)
        self.assertEqual(set([0, 3]), x)        


    def test_adjust_coordinates(self):
        x = main1.adjust_coordinates((3, 4), [9], [9])
        self.assertEqual((3, 4), x)
        x = main1.adjust_coordinates((13, 4), [9], [9])
        self.assertEqual((14, 4), x)        
        x = main1.adjust_coordinates((3, 14), [9], [9])
        self.assertEqual((3, 15), x)
        x = main1.adjust_coordinates((31, 41), [9, 1], [9, 10])
        self.assertEqual((33, 43), x)
