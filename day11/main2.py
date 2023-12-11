import time

from typing import Set


def main():
    original_galaxies = get_galaxies()
    expanding_rows, expanding_columns = get_expanding_rows(original_galaxies), get_expanding_columns(original_galaxies)
    adjusted_galaxies = get_adjusted_galaxies(original_galaxies, expanding_rows, expanding_columns)
    total = calculate_total_distance(adjusted_galaxies)
    print(total)


def get_galaxies():
    result = set()
    for row, line in enumerate(get_lines()):
        for col, char in enumerate(list(line)):
            if char == '#':
                result.add((row, col))
    return result


def get_adjusted_galaxies(galaxies, expanding_rows, expanding_columns):
    return [adjust_coordinates(galaxy, expanding_rows, expanding_columns) for galaxy in galaxies]


def adjust_coordinates(galaxy, expanding_rows, expanding_columns):
    adjustment_factor = 1000000 - 1
    row = galaxy[0] + (adjustment_factor * len([x for x in expanding_rows if x < galaxy[0]]))
    col = galaxy[1] + (adjustment_factor * len([x for x in expanding_columns if x < galaxy[1]]))
    return (row, col)


def get_expanding_rows(galaxies):
    return get_missing_values(set([galaxy[0] for galaxy in galaxies]))


def get_expanding_columns(galaxies):
    return get_missing_values(set([galaxy[1] for galaxy in galaxies]))


def get_missing_values(s: Set[int]):
    return set(range(max(s))) - s


def calculate_total_distance(galaxies):
    result = 0
    for galaxy1 in galaxies:
        for galaxy2 in galaxies:
            if galaxy1 < galaxy2:
                result += calculate_manhattan_distance(galaxy1, galaxy2)
    return result


def calculate_manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
