import argparse
import re
import time

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Tuple

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()

input_pattern1 = re.compile("([UDLR]) ([1-9][0-9]*) .+")
input_pattern2 = re.compile("[^#]+#(.{5})([0123])\\)")


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


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def move(self, direction: Direction, units: int = 1):
        row = self.row + (direction.value[0] * units)
        col = self.col + (direction.value[1] * units)
        return Coordinate(row, col)


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


@dataclass(frozen=True)
class LineSegment:
    endpoints: tuple[Coordinate, Coordinate]

    def __init__(self, c1: Coordinate, c2: Coordinate):
        object.__setattr__(self, "endpoints", (c1, c2))

    @property
    def orientation(self):
        if self.endpoints[0].row == self.endpoints[1].row:
            return Orientation.HORIZONTAL
        else:
            return Orientation.VERTICAL

    @property
    def row(self):
        return self.endpoints[0].row if self.orientation == Orientation.HORIZONTAL else None

    @property
    def col(self):
        return self.endpoints[0].col if self.orientation == Orientation.VERTICAL else None

    def crosses_row(self, row: int) -> bool:
        if self.orientation == Orientation.VERTICAL:
            rows = [x.row for x in self.endpoints]
            return min(rows) <= row <= max(rows)
        return False


class LineSegmentCollection:

    def __init__(self, line_segments: List[LineSegment]):
        self._line_segments = line_segments[:]

    def __len__(self):
        return len(self._line_segments)

    def __getitem__(self, index) -> LineSegment:
        return self._line_segments[index % len(self._line_segments)]

    def get_by_orientation(self, orientation: Orientation):
        return [x for x in self._line_segments if x.orientation == orientation]

    def get_horizontal_by_row_number(self, row_number: int) -> List[LineSegment]:
        return [x for x in self._line_segments if x.orientation == Orientation.HORIZONTAL and x.row == row_number]

    def get_vertical_by_row_number(self, row_number: int) -> List[int]:
        return [x.col for x in self._line_segments if x.orientation == Orientation.VERTICAL and x.crosses_row(row_number)]

    def is_u_turn(self, row, col1, col2):
        for i in range(len(self._line_segments)):
            ls = self._line_segments[i]
            if ls.orientation == Orientation.HORIZONTAL and ls.row == row:
                cols = [x.col for x in ls.endpoints]
                if col1 in cols and col2 in cols:
                    return self._is_u_turn(i)
        raise Exception("'Balh")

    def _is_u_turn(self, index):
        # a and c are the neighbors of b.
        # return true if a and c point in the same direction.
        b = self[index]
        a, c = self[index-1], self[index+1]
        return (a.endpoints[0].row < b.row) == (c.endpoints[1].row < b.row)


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():
    line_segment_collection = get_line_segment_collection()
    terrain_width = max([x.col for x in line_segment_collection.get_by_orientation(Orientation.VERTICAL)]) + 1
    rows = sorted(set([x.row for x in line_segment_collection.get_by_orientation(Orientation.HORIZONTAL)]))
    total_area = 0
    for row in rows:
        area = calculate_row_area(row, line_segment_collection, terrain_width)
        total_area += area
    for i in range(1, len(rows)):
        r1, r2 = rows[i-1] + 1, rows[i] - 1
        if r1 <= r2:
            height = r2 - r1 + 1
            width = calculate_row_area(r1, line_segment_collection, terrain_width)
            area = height * width
            total_area += area
    print(total_area)


def get_line_segment_collection() -> LineSegmentCollection:
    line_segments = get_line_segments2()
    return LineSegmentCollection(line_segments)


def get_line_segments1() -> List[LineSegment]:
    coordinates: List[Coordinate] = [Coordinate(0, 0)]
    for line in get_lines():
        match = input_pattern1.fullmatch(line)
        direction, distance = match.group(1), match.group(2)
        direction, distance = Direction.from_string(direction), int(distance)
        coordinates.append(coordinates[-1].move(direction, distance))
    result: List[LineSegment] = []
    for i in range(1, len(coordinates)):
        result.append(LineSegment(coordinates[i-1], coordinates[i]))
    return result


def get_line_segments2() -> List[LineSegment]:
    coordinates: List[Coordinate] = [Coordinate(0, 0)]
    for line in get_lines():
        match = input_pattern2.fullmatch(line)
        direction, distance = match.group(2), match.group(1)
        direction, distance = "RDLU"[int(direction)], int(distance, 16)
        direction = Direction.from_string(direction)
        coordinates.append(coordinates[-1].move(direction, distance))
    result: List[LineSegment] = []
    for i in range(1, len(coordinates)):
        result.append(LineSegment(coordinates[i-1], coordinates[i]))
    return result


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


class RowAreaCalculationType(Enum):
    ROW = 1
    COL = 2
    OUTSIDE = 3
    UNKNOWN = 4
    INSIDE = 5

    def opposite(self):
        if self == RowAreaCalculationType.OUTSIDE:
            return RowAreaCalculationType.INSIDE
        if self == RowAreaCalculationType.INSIDE:
            return RowAreaCalculationType.OUTSIDE
        raise Exception(f"{self} has no opposite")


class RowAreaCalculationNode:

    def __init__(self, type: RowAreaCalculationType, start: int, end: int):
        self.type = type
        self.start = start
        self.end = end

    def __repr__(self):
        return f"RowAreaCalculationNode(type={self.type}, start={self.start}, end={self.end})"

    def __lt__(self, other):
        return self.start < other.start

    def __len__(self):
        return self.end - self.start + 1


def calculate_row_area(row_number: int, line_segment_collection: LineSegmentCollection, terrain_width):
    nodes: List[RowAreaCalculationNode] = []
    columns_covered_by_rows = set()
    for ls in line_segment_collection.get_horizontal_by_row_number(row_number):
        columns_covered_by_rows.add(ls.endpoints[0].col)
        columns_covered_by_rows.add(ls.endpoints[1].col)
        cols = [x.col for x in ls.endpoints]
        nodes.append(RowAreaCalculationNode(RowAreaCalculationType.ROW, min(cols), max(cols)))
    for col in line_segment_collection.get_vertical_by_row_number(row_number):
        if col not in columns_covered_by_rows:
            nodes.append(RowAreaCalculationNode(RowAreaCalculationType.COL, col, col))
    unknown_ranges = []
    current_start = 0
    nodes = [x for x in sorted(nodes)]
    for node in nodes:
        if node.start > current_start:
            unknown_ranges.append(RowAreaCalculationNode(RowAreaCalculationType.UNKNOWN, current_start, node.start - 1))
        current_start = node.end + 1
    if current_start < terrain_width:
        unknown_ranges.append(RowAreaCalculationNode(RowAreaCalculationType.UNKNOWN, current_start, terrain_width))
    nodes.extend(unknown_ranges)
    nodes = [x for x in sorted(nodes)]
    for i in [0, -1]:
        if nodes[i].type == RowAreaCalculationType.UNKNOWN:
            nodes[i].type = RowAreaCalculationType.OUTSIDE
    for i, node in enumerate(nodes):
        if node.type == RowAreaCalculationType.UNKNOWN:
            if i-2 < 0:
                node.type = RowAreaCalculationType.INSIDE
            elif nodes[i-1].type == RowAreaCalculationType.COL:
                node.type = nodes[i-2].type.opposite()
            elif nodes[i-1].type == RowAreaCalculationType.ROW:
                if line_segment_collection.is_u_turn(row_number, nodes[i-1].start, nodes[i-1].end):
                    node.type = nodes[i-2].type
                else:
                    node.type = nodes[i-2].type.opposite()
    return sum([len(x) for x in nodes if x.type != RowAreaCalculationType.OUTSIDE])


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
