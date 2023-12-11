import unittest

from main1 import Landscape, Tile, pipes

class Test1(unittest.TestCase):

    def test_landscape_add(self):
        north_south = [x for x in pipes if x.char == '|'][0]
        landscape = Landscape()
        landscape.add(Tile(1, 2, north_south))
        x = landscape.get_tile(1, 2)
        self.assertEqual(1, x.row)
        self.assertEqual(2, x.col)
        self.assertEqual('|', x.pipe.char)

    def test_landscape_get_neighbors1(self):
        north_south = [x for x in pipes if x.char == '|'][0]
        east_west = [x for x in pipes if x.char == '-'][0]
        landscape = Landscape()
        landscape.add(Tile(2, 5, north_south))
        landscape.add(Tile(3, 5, north_south))
        x = landscape.get_neighbors(3, 5)
        self.assertEqual(1, len(x))
        x = x[0]
        self.assertIsNotNone(x)
        self.assertEqual(2, x.row)
        self.assertEqual(5, x.col)
        self.assertEqual('|', x.pipe.char)
    
    def test_landscape_get_neighbors2(self):
        north_south = [x for x in pipes if x.char == '|'][0]
        east_west = [x for x in pipes if x.char == '-'][0]
        landscape = Landscape()
        landscape.add(Tile(2, 5, north_south))
        landscape.add(Tile(3, 5, east_west))
        x = landscape.get_neighbors(3, 5)
        self.assertEqual(0, len(x))

    def test_landscape_get_neighbors3(self):
        north_south = [x for x in pipes if x.char == '|'][0]
        east_west = [x for x in pipes if x.char == '-'][0]
        landscape = Landscape()
        landscape.add(Tile(2, 5, east_west))
        landscape.add(Tile(3, 5, north_south))
        x = landscape.get_neighbors(3, 5)
        self.assertEqual(0, len(x))
