import re
import time

from dataclasses import dataclass

integers_pattern = re.compile('[0-9]+')


@dataclass
class Race:
    duration: int
    distance_to_beat: int


def main():
    race = get_race()
    total = count_ways_to_win(race)
    print(total)


def count_ways_to_win(race: Race):
    result = 0
    for button_press in range(race.duration):
        velocity = button_press
        distance_travelled = velocity * (race.duration - button_press)
        if distance_travelled > race.distance_to_beat:
            result += 1
    return result


def get_race():
    lines = get_lines()
    time = int(''.join([str(x) for x in find_all_integers(next(lines))]))
    distance = int(''.join([str(x) for x in find_all_integers(next(lines))]))
    return Race(time, distance)


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
