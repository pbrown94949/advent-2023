import re
import time

from dataclasses import dataclass
from typing import List

integers_pattern = re.compile('[0-9]+')
map_start_pattern = re.compile('([a-z]+)-to-([a-z]+) map:')


@dataclass(frozen=True)
class TransformationRule:
    destination_range_start: int
    source_range_start: int
    range_length: int

    def can_transform(self, value):
        return value >= self.source_range_start and value < self.source_range_start + self.range_length

    def transform(self, value):
        return self.destination_range_start + value - self.source_range_start


@dataclass(frozen=True)
class Map:
    source_category: str
    destination_category: str
    transformation_rules: List[TransformationRule]

    def transform(self, value):
        for rule in self.transformation_rules:
            if rule.can_transform(value):
                return rule.transform(value)
        return value


@dataclass(frozen=True)
class MapManager:
    maps: List[Map]

    def transform(self, source_category, value):
        for map in self.maps:
            if map.source_category == source_category:
                return map.destination_category, map.transform(value)
        raise Exception(f'No map found for {source_category}')


def main():
    map_manager = build_map_manager()
    min_location = None
    for seed in get_seeds():
        location = get_location(seed, map_manager)
        if min_location is None or min_location > location:
            min_location = location
    print(f'Minimum location: {min_location}')


def get_seeds():
    line = next(get_lines())
    return find_all_integers(line)


def build_map_manager():
    maps = []
    for source_category, destination_category, rule_values in get_map_input():
        rules = [TransformationRule(*r) for r in rule_values]
        map = Map(source_category, destination_category, rules)
        maps.append(map)
    return MapManager(maps)


def get_map_input():
    generator = get_lines()
    for line in generator:
        match = map_start_pattern.fullmatch(line)
        if match:
            source_category, destination_category = match.group(
                1), match.group(2)
            rules = []
            for line in generator:
                if line != '':
                    rules.append(find_all_integers(line))
                else:
                    yield source_category, destination_category, rules
                    break
    yield source_category, destination_category, rules


def get_location(seed, map_manager):
    category, value = 'seed', seed
    while category != 'location':
        category, value = map_manager.transform(category, value)
    return value


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
