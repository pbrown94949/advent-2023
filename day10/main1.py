import collections
import time

from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Pipe:
    char: str
    openings: List[str]


@dataclass
class Tile:
    row: int
    col: int
    pipe: Pipe
    distance: int = None


class Landscape:

    def __init__(self):
        self._dict = {}
        self._max_row = self._max_col = None

    def add(self, tile: Tile):
        self._dict[(tile.row, tile.col)] = tile
        if self._max_row is None or self._max_row < tile.row:
            self._max_row = tile.row
        if self._max_col is None or self._max_col < tile.col:
            self._max_col = tile.col

    def get_tile(self, row, col) -> Tile:
        return self._dict.get((row, col), None)

    def get_tiles(self) -> List[Tile]:
        return [tile for tile in self._dict.values()]

    def get_neighbors(self, row, col) -> List[Tile]:
        result = []
        tile = self.get_tile(row, col)
        if tile:
            result = [self._get_neighbor(row, col, direction) for direction in tile.pipe.openings]
        return [x for x in result if x]

    def _get_neighbor(self, row, col, direction):
        if direction == 'north':
            row -= 1
            opposite_direction = 'south'
        if direction == 'south':
            row += 1
            opposite_direction = 'north'
        if direction == 'east':
            col += 1
            opposite_direction = 'west'
        if direction == 'west':
            col -= 1
            opposite_direction = 'east'
        temp = self.get_tile(row, col)
        return temp if temp and opposite_direction in temp.pipe.openings else None

    @property
    def height(self):
        return self._max_row + 1

    @property
    def width(self):
        return self._max_col + 1


pipes = [
    Pipe('|', ['north', 'south']),
    Pipe('-', ['east', 'west']),
    Pipe('L', ['north', 'east']),
    Pipe('J', ['north', 'west']),
    Pipe('7', ['south', 'west']),
    Pipe('F', ['south', 'east']),
    Pipe('.', []),
    Pipe('S', ['north', 'south', 'east', 'west'])
]


def main():
    landscape = build_landscape()
    start_tile = find_start_location(landscape)
    start_tile.distance = 0
    process_tile(start_tile, landscape)
    print_result(landscape)

def build_landscape():
    result = Landscape()
    for row, line in enumerate(get_lines()):
        for col, char in (enumerate(list(line))):
            result.add(Tile(row, col, [pipe for pipe in pipes if pipe.char == char][0]))
    return result


def find_start_location(landscape: Landscape) -> Tile:
    for tile in landscape.get_tiles():
        if tile.pipe.char == 'S':
            return tile
    return None


def process_tile(tile: Tile, landscape: Landscape):
    queue = collections.deque()
    queue.append(tile)
    while len(queue) > 0:
        tile = queue.popleft()
        neighbors = landscape.get_neighbors(tile.row, tile.col)
        for neighbor in neighbors:
            if neighbor.distance is None or neighbor.distance > tile.distance + 1:
                neighbor.distance = tile.distance + 1
                queue.append(neighbor)


def print_distances(landscape: Landscape):
    for row in range(landscape.height):
        for col in range(landscape.width):
            tile = landscape.get_tile(row, col)
            if tile is None or tile.distance is None:
                print('.', end="")
            else:
                print(tile.distance, end="")
        print()

def print_result(landscape: Landscape):
    max_distance = 0
    for tile in landscape.get_tiles():
        if tile.distance and max_distance < tile.distance:
            max_distance = tile.distance
    print(max_distance)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
