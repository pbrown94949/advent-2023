import re
import time

from dataclasses import dataclass
from typing import List

integers_pattern = re.compile('[0-9]+')
map_start_pattern = re.compile('([a-z]+)-to-([a-z]+) map:')


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        return self.end < other.end

    def __repr__(self):
        return f"Range({self.start:,}, {self.end:,})"

    def overlaps_with(self, other):
        return max(self.start, other.start) <= min(self.end, other.end)


def build_range(start, length):
    return Range(start, start + length - 1)


def adjust_range(range: Range, adjustment: int):
    return Range(range.start + adjustment, range.end + adjustment)


@dataclass(frozen=True)
class Transformation:
    start: int
    end: int
    adjustment: int

    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        return self.end < other.end

    def covers(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps_with(self, other):
        return max(self.start, other.start) <= min(self.end, other.end)

    def split_range(self, range: Range) -> List[Range]:
        if not self.overlaps_with(range):
            return [range]
        result = [Range(max(range.start, self.start), min(range.end, self.end))]
        if range.start < result[0].start:
            result.append(Range(range.start, result[0].start - 1))
        if range.end > result[0].end:
            result.append(Range(result[0].end + 1, range.end))
        return sorted(result)


def build_transformation(destination_range_start, source_range_start, range_length):
    start = source_range_start
    end = source_range_start + range_length - 1
    adjustment = destination_range_start - source_range_start
    return Transformation(start, end, adjustment)


@dataclass(frozen=True)
class Map:
    source_category: str
    destination_category: str
    transformations: List[Transformation]

    def split_ranges(self, ranges: List[Range]):
        return self._split_ranges(ranges, self.transformations)

    def _split_ranges(self, ranges: List[Range], transformations: List[Transformation]):
        if len(transformations):
            transformed_ranges = []
            for range in ranges:
                transformed_ranges.extend(transformations[0].split_range(range))
            return self._split_ranges(transformed_ranges, transformations[1:])
        else:
            return ranges

    def transform_ranges(self, ranges: List[Range]) -> List[Range]:
        result = []
        for range in ranges:
            transformation = self._find_transformation(range)
            result.append(adjust_range(range, transformation.adjustment) if transformation else range)
        return result

    def _find_transformation(self, range: Range) -> Transformation:
        temp = [t for t in self.transformations if t.covers(range)]
        if len(temp) > 1:
            raise Exception('Too many transformations found')
        if len(temp):
            return temp[0]
        return None


class MapHolder:

    def __init__(self):
        self._maps: List[Map] = []

    def add_map(self, map: Map):
        self._maps.append(map)

    def get_map(self, source_category):
        for map in self._maps:
            if map.source_category == source_category:
                return map
        return None


def main():
    ranges = build_seed_ranges()
    holder = build_map_holder()
    map = holder.get_map('seed')
    while map:
        ranges = map.split_ranges(ranges)
        ranges = map.transform_ranges(ranges)
        map = holder.get_map(map.destination_category)
    ranges.sort()
    print(ranges[0].start)


def build_seed_ranges():
    result = []
    seed_input = get_seed_input()
    for start_seed, length in zip(seed_input[0::2], seed_input[1::2]):
        result.append(build_range(start_seed, length))
    return sorted(result)


def get_seed_input():
    return find_all_integers(next(get_lines()))


def build_map_holder():
    result = MapHolder()
    for source_category, destination_category, transformation_parameters in get_map_input():
        transformations = [build_transformation(*x) for x in transformation_parameters]
        map = Map(source_category, destination_category, transformations)
        result.add_map(map)
    return result


def get_map_input():
    generator = get_lines()
    for line in generator:
        match = map_start_pattern.fullmatch(line)
        if match:
            source_category, destination_category = match.group(1), match.group(2)
            transformation_parameters = []
            for line in generator:
                if line != '':
                    transformation_parameters.append(find_all_integers(line))
                else:
                    yield source_category, destination_category, transformation_parameters
                    break
    yield source_category, destination_category, transformation_parameters


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


def find_all_integers(line):
    return [int(x) for x in integers_pattern.findall(line)]


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
