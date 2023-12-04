import re
import time

from dataclasses import dataclass
from typing import List

number_pattern = re.compile('([1-9][0-9]*)')


@dataclass
class PartNumber:
    value: int
    row: int
    col_start: int
    col_end: int

    def includes_any_point(self, points):
        for row, col in points:
            if self.includes_point(row, col):
                return True
        return False

    def includes_point(self, row, col):
        return self.row == row and self.col_start <= col and col <= self.col_end


def main():
    total = 0
    numbers = get_numbers()
    for row, col in get_gear_locations():
        neighbors = get_neighbors(row, col)
        adjacent_numbers = [
            x for x in numbers if x.includes_any_point(neighbors)]
        if len(adjacent_numbers) == 2:
            gear_ratio = adjacent_numbers[0].value * adjacent_numbers[1].value
            total += gear_ratio
    print(total)


def get_numbers() -> List[PartNumber]:
    result = []
    for row, line in enumerate(get_lines()):
        for match in number_pattern.finditer(line):
            result.append(PartNumber(int(match.group(1)), row,
                          match.start(1), match.end(1) - 1))
    return result


def get_gear_locations():
    for row, line in enumerate(get_lines()):
        for col, char in enumerate(list(line)):
            if char == '*':
                yield row, col


def get_neighbors(row, col):
    result = set()
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if a != 0 or b != 0:
                result.add((row + a, col + b))
    return result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
