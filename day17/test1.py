import unittest

import main1


class Test1(unittest.TestCase):

    def test_east_west(self):
        left, right = main1.Node(2, 3, 0), main1.Node(2, 4, 0)
        response = main1.get_direction_of_travel(left, right)
        self.assertEqual('e', response)
        response = main1.get_direction_of_travel(right, left)
        self.assertEqual('w', response)

    def test_north_south(self):
        up, down = main1.Node(5, 3, 0), main1.Node(6, 3, 0)
        response = main1.get_direction_of_travel(up, down)
        self.assertEqual('s', response)
        response = main1.get_direction_of_travel(down, up)
        self.assertEqual('n', response)
