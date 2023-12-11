import collections
import time

from dataclasses import dataclass, field
from typing import List, Dict, Generic, Tuple, TypeVar


directions = ['north', 'south', 'east', 'west']


def get_opposite_direction(direction: str):
    idx = directions.index(direction)
    if idx % 2 == 0:
        return directions[idx + 1]
    return directions[idx - 1]


@dataclass(frozen=True)
class Pipe:
    char: str
    openings: List[str]


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


def find_pipe(char: str):
    return [pipe for pipe in pipes if pipe.char == char][0]


def can_connect(pipe_from: Pipe, pipe_to: Pipe, direction_from: str):
    return get_opposite_direction(direction_from) in pipe_from.openings and direction_from in pipe_to.openings


@dataclass
class PipeTile:
    row: int
    col: int
    pipe: Pipe
    distance: int = None


T = TypeVar("T")


class CompassGrid(Generic[T]):

    def __init__(self):
        self._dict = {}
        self._max_row = self._max_col = None

    def put_item(self, row, col, item: T):
        self._dict[(row, col)] = item
        if self._max_row is None or self._max_row < row:
            self._max_row = row
        if self._max_col is None or self._max_col < col:
            self._max_col = col

    def get_item(self, row, col) -> T:
        return self._dict.get((row, col), None)

    def get_items(self) -> List[T]:
        return [tile for tile in self._dict.values()]

    def get_neighbor(self, row, col, direction) -> T:
        if direction == 'north':
            row -= 1
        elif direction == 'south':
            row += 1
        elif direction == 'east':
            col += 1
        elif direction == 'west':
            col -= 1
        else:
            raise Exception('Invalid direction')
        return self.get_item(row, col)

    def get_neighbors(self, row, col) -> List[T]:
        result = [self.get_neighbor(row, col, direction) for direction in directions]
        return [x for x in result if x]

    @property
    def height(self):
        return self._max_row + 1

    @property
    def width(self):
        return self._max_col + 1


def main():
    landscape = build_landscape()
    start_tile = find_start_location(landscape)
    start_tile.distance = 0
    process_tile(start_tile, landscape)
    #print_landscape(landscape)
    #print_distances(landscape)
    working_grid = build_working_grid(landscape)
    mark_outside(working_grid)
    mark_inside(working_grid)
    #print_string_grid(working_grid)
    results_grid = build_results_grid(landscape, working_grid)
    print_string_grid(results_grid)
    print_result(results_grid)


def build_landscape():
    result = CompassGrid[PipeTile]()
    for row, line in enumerate(get_lines()):
        for col, char in (enumerate(list(line))):
            result.put_item(row, col, PipeTile(row, col, find_pipe(char)))
    return result


def find_start_location(landscape: CompassGrid[PipeTile]) -> PipeTile:
    for tile in landscape.get_items():
        if tile.pipe.char == 'S':
            return tile
    return None


def process_tile(tile: PipeTile, landscape: CompassGrid[PipeTile]):
    queue = collections.deque()
    queue.append(tile)
    while len(queue) > 0:
        tile = queue.popleft()
        for direction in directions:
            neighbor = landscape.get_neighbor(tile.row, tile.col, direction)
            if neighbor and neighbor.distance is None and can_connect(neighbor.pipe, tile.pipe, direction):
                neighbor.distance = tile.distance + 1
                queue.append(neighbor)


def build_working_grid(landscape: CompassGrid[str]):
    result = CompassGrid[str]()
    for row in range(landscape.height * 2 + 1):
        for col in range(landscape.width * 2 + 1):
            result.put_item(row, col, ' ')
    for row in range(landscape.height):
        for col in range(landscape.width):
            tile: PipeTile = landscape.get_item(row, col)
            if tile.pipe.char != '.' and tile.distance is not None:
                result.put_item(row * 2 + 1, col * 2 + 1, '#')
            south = landscape.get_neighbor(row, col, 'south')
            if south and can_connect(tile.pipe, south.pipe, 'north'):
                result.put_item(row * 2 + 2, col * 2 + 1, '+')
            east = landscape.get_neighbor(row, col, 'east')
            if east and can_connect(tile.pipe, east.pipe, 'west'):
                result.put_item(row * 2 + 1, col * 2 + 2, '+')
    return result


def mark_outside(grid: CompassGrid[str]):
    for row in range(grid.height):
        for col in range(grid.width):
            if row == 0 or col == 0:
                grid.put_item(row, col, 'O')
    keep_running = True
    while keep_running:
        keep_running = False
        for row in range(grid.height):
            for col in range(grid.width):
                if grid.get_item(row, col) == ' ':
                    is_outside = 'O' in grid.get_neighbors(row, col)
                    if is_outside:
                        grid.put_item(row, col, 'O')
                        keep_running = True


def mark_inside(pipe_grid: CompassGrid[str]):
    keep_running = True
    while keep_running:
        keep_running = False
        for row in range(pipe_grid.height):
            for col in range(pipe_grid.width):
                if pipe_grid.get_item(row, col) == ' ':
                    keep_running = True
                    pipe_grid.put_item(row, col, 'I')


def build_results_grid(landscape: CompassGrid[PipeTile], working_grid: CompassGrid[str]):
    result = CompassGrid[str]()
    for row in range(landscape.height):
        for col in range(landscape.width):
            adj_row, adj_col = row * 2 + 1, col * 2 + 1
            result.put_item(row, col, working_grid.get_item(adj_row, adj_col))
    return result


def print_landscape(landscape: CompassGrid[PipeTile]):
    for row in range(landscape.height):
        for col in range(landscape.width):
            tile = landscape.get_item(row, col)
            print(tile.pipe.char, end="")
        print()


def print_distances(landscape: CompassGrid[PipeTile]):
    for row in range(landscape.height):
        for col in range(landscape.width):
            tile = landscape.get_item(row, col)
            if tile is None or tile.distance is None:
                print('.', end="")
            else:
                print(tile.distance, end="")
        print()


def print_string_grid(grid: CompassGrid[str]):
    for row in range(grid.height):
        for col in range(grid.width):
            print(grid.get_item(row, col), end="")
        print()


def print_result(grid: CompassGrid[str]):
    total = 0
    for row in range(grid.height):
        for col in range(grid.width):
            if grid.get_item(row, col) == 'I':
                total += 1
    print(total)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
