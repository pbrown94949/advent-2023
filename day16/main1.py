import time

from dataclasses import dataclass
from typing import List, Set


class Tile:
    action: str
    row: int
    col: int
    visitors: Set[str]

    def __init__(self, action, row, col):
        self.action = action
        self.row, self.col = row, col
        self.visitors = set()

    def __repr__(self):
        return f"Tile(action={self.action}, row={self.row}, col={self.col}, visited={self.visited}, visitors={self.visitors})"

    @property
    def visited(self):
        return len(self.visitors) > 0

forward_motion_map = {
    'n': (-1, 0),
    's': (1, 0),
    'e': (0, 1),
    'w': (0, -1)
}


def calculate_forward_motion(direction):
    return forward_motion_map[direction]

clockwise_directions = ['n', 'e', 's', 'w']
counterclockwise_directions = clockwise_directions[::-1]


def calculate_left_direction(direction):
    idx = clockwise_directions.index(direction) - 1
    return clockwise_directions[idx]


def calculate_right_direction(direction):
    idx = counterclockwise_directions.index(direction) - 1
    return counterclockwise_directions[idx]


@dataclass(frozen=True)
class Cursor:
    direction: str
    row: int
    col: int

    def go_forward(self):
        row_adj, col_adj = calculate_forward_motion(self.direction)
        return Cursor(self.direction, self.row + row_adj, self.col + col_adj)

    def go_left(self):
        cursor = Cursor(calculate_left_direction(self.direction), self.row, self.col)
        return cursor.go_forward()

    def go_right(self):
        cursor = Cursor(calculate_right_direction(self.direction), self.row, self.col)
        return cursor.go_forward()

    @property
    def is_east_west(self):
        return self.direction == 'e' or self.direction == 'w'


class Tiles:

    def __init__(self):
        self._tiles = []

    def add(self, tile):
        self._tiles.append(tile)

    def get(self, row, col) -> Tile:
        temp = [tile for tile in self._tiles if tile.row == row and tile.col == col]
        return temp[0] if temp else None

    def count_visited(self):
        result = 0
        for tile in self._tiles:
            if tile.visited:
                result += 1
        return result


def main():
    tiles = get_tiles()
    tiles.get(0, 0).visitors.add('e')
    cursors = [Cursor('e', 0, 0)]
    while len(cursors) > 0:
        cursors = move_cursors(cursors, tiles)
        cursors = prune_cursors(cursors, tiles)
        apply_cursors(cursors, tiles)
    print(tiles.count_visited())


def get_tiles():
    result = Tiles()
    for row, line in enumerate(get_lines()):
        for col, char in enumerate(list(line)):
            result.add(Tile(char, row, col))
    return result


def move_cursors(cursors: List[Cursor], tiles: Tiles) -> List[Cursor]:
    result = []
    for cursor in cursors:
        result.extend(move_cursor(cursor, tiles))
    return result


movement_map = {
    ('.', True): ['forward'],
    ('.', False): ['forward'],
    ('|', True): ['left', 'right'],
    ('|', False): ['forward'],
    ('-', True): ['forward'],
    ('-', False): ['left', 'right'],
    ('\\', True): ['right'],
    ('\\', False): ['left'],
    ('/', True): ['left'],
    ('/', False): ['right']
}


def move_cursor(cursor: Cursor, tiles: Tiles) -> List[Cursor]:
    tile = tiles.get(cursor.row, cursor.col)
    movements = movement_map[(tile.action, cursor.is_east_west)]
    result = []
    if 'forward' in movements:
        result.append(cursor.go_forward())
    if 'left' in movements:
        result.append(cursor.go_left())
    if 'right' in movements:
        result.append(cursor.go_right())
    return result


def prune_cursors(cursors: List[Cursor], tiles: Tiles) -> List[Cursor]:
    result = []
    for cursor in cursors:
        tile = tiles.get(cursor.row, cursor.col)
        if tile is not None and cursor.direction not in tile.visitors:
            result.append(cursor)
    return result


def apply_cursors(cursors: List[Cursor], tiles: Tiles):
    for cursor in cursors:
        tile = tiles.get(cursor.row, cursor.col)
        tile.visitors.add(cursor.direction)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
