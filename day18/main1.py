import argparse
import collections
import re
import time

from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Tuple

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()

input_pattern = re.compile("([UDLR]) ([1-9][0-9]*) .+")


class Direction(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)

    @classmethod
    def from_string(cls, str):
        for k, v in cls.__members__.items():
            if k == str:
                return v
        else:
            raise Exception(f"not found: {str}")


class BlockType(Enum):
    DITCH = "DITCH"
    OUTSIDE = "OUTSIDE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def move(self, direction: Direction, units: int = 1):
        row = self.row + (direction.value[0] * units)
        col = self.col + (direction.value[1] * units)
        return Coordinate(row, col)

    def translate_to_zero_based(self, row_adjustment, col_adjustment):
        row = self.row - row_adjustment
        col = self.col - col_adjustment
        return Coordinate(row, col)

    def translate_from_zero_based(self, row_adjustment, col_adjustment):
        row = self.row + row_adjustment
        col = self.col + col_adjustment
        return Coordinate(row, col)


class Matrix[T]:

    def __init__(self, height, width):
        self._height, self._width = height, width
        self._array = []
        for _ in range(height):
            self._array.append([None for _ in range(width)])

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def get(self, c: Coordinate) -> T:
        return self._array[c.row][c.col]

    def put(self, c: Coordinate, item: T):
        self._array[c.row][c.col] = item

    def get_neighbors(self, c: Coordinate) -> List[Tuple[Coordinate, T]]:
        return [(n, self.get(n)) for n in self._get_neighbor_coordinates(c)]

    def _get_neighbor_coordinates(self, c: Coordinate) -> List[Coordinate]:
        result = []
        for direction in Direction:
            neighbor = c.move(direction)
            if 0 <= neighbor.row < len(self._array) and 0 <= neighbor.col < len(self._array[0]):
                result.append(neighbor)
        return result


class NonOriginBasedMatrix[T]:

    def __init__(self, min_row, max_row, min_col, max_col):
        self._matrix = Matrix(max_row - min_row + 1, max_col - min_col + 1)
        self._min_row, self._min_col = min_row, min_col

    @property
    def height(self):
        return self._matrix.height

    @property
    def width(self):
        return self._matrix.width

    @property
    def min_row(self):
        return self._min_row

    @property
    def min_col(self):
        return self._min_col

    def get(self, c: Coordinate) -> T:
        zero_based_coordinate = c.translate_to_zero_based(self._min_row, self._min_col)
        return self._matrix.get(zero_based_coordinate)

    def put(self, c: Coordinate, item: T):
        zero_based_coordinate = c.translate_to_zero_based(self._min_row, self._min_col)
        self._matrix.put(zero_based_coordinate, item)

    def get_neighbors(self, c: Coordinate) -> List[T]:
        zero_based_coordinate = c.translate_to_zero_based(self._min_row, self._min_col)
        result = []
        for item_coordinate, item in self._matrix.get_neighbors(zero_based_coordinate):
            nonzero_based_coordinate = item_coordinate.translate_from_zero_based(self._min_row, self._min_col)
            result.append((nonzero_based_coordinate, item))
        return result


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():

    ditch_coordinates = get_ditch_coordinates()
    min_row, max_row, min_col, max_col = get_min_max_coordinates(ditch_coordinates)
    print(min_row, max_row, min_col, max_col)
    edge_coordinates = get_edge_coordinates(min_row, max_row, min_col, max_col)
    outside_coordinates = set([x for x in edge_coordinates if x not in ditch_coordinates])
    matrix = NonOriginBasedMatrix[BlockType](min_row, max_row, min_col, max_col)
    for c in ditch_coordinates:
        matrix.put(c, BlockType.DITCH)
    for c in outside_coordinates:
        matrix.put(c, BlockType.OUTSIDE)
    queue = collections.deque()
    queue.extend(outside_coordinates)
    while queue:
        c = queue.popleft()
        neighbors = matrix.get_neighbors(c)
        for neighbor_coordinate, neighbor in neighbors:
            if neighbor is None:
                matrix.put(neighbor_coordinate, BlockType.OUTSIDE)
                queue.append(neighbor_coordinate)
    lava_cubes = 0
    for row in range(matrix.height):
        row += matrix.min_row
        for col in range(matrix.width):
            col += matrix.min_col
            block = matrix.get(Coordinate(row, col))
            if block != BlockType.OUTSIDE:
                lava_cubes += 1
    print(lava_cubes)
    for row in range(matrix.height):
        row += matrix.min_row
        for col in range(matrix.width):
            col += matrix.min_col
            block = matrix.get(Coordinate(row, col))
            if block == BlockType.OUTSIDE:
                char = '.'
            elif block == BlockType.DITCH:
                char = '#'
            else:
                char = ' '
            print(char, end='')
        print()


def get_ditch_coordinates():
    result = set()
    c = Coordinate(0, 0)
    result.add(c)
    for line in get_lines():
        match = input_pattern.fullmatch(line)
        direction, distance = match.group(1), match.group(2)
        direction, distance = Direction.from_string(direction), int(distance)
        for _ in range(distance):
            c = c.move(direction)
            result.add(c)
    return result


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def get_min_max_coordinates(coordinates: Set[Coordinate]):
    for c in coordinates:
        min_row, max_row, min_col, max_col = c.row, c.row, c.col, c.col
        break
    for c in coordinates:
        min_row = min(min_row, c.row)
        max_row = max(max_row, c.row)
        min_col = min(min_col, c.col)
        max_col = max(max_col, c.col)
    return min_row, max_row, min_col, max_col


def get_edge_coordinates(min_row, max_row, min_col, max_col):
    result = set()
    for row in range(min_row, max_row + 1):
        result.add(Coordinate(row, min_col))
        result.add(Coordinate(row, max_col))
    for col in range(min_col, max_col + 1):
        result.add(Coordinate(min_row, col))
        result.add(Coordinate(max_row, col))
    return result


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
