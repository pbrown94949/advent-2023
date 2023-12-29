import time

stop = 1000000000


def main():
    non_repeating_count, repeating_maps_length = analyze_map_pattern()
    cycles_needed = ((stop - non_repeating_count) % repeating_maps_length) + non_repeating_count
    map = get_map()
    for i in range(cycles_needed):
        perform_cycle(map)
    load = calculate_load(map)
    print(load)


def analyze_map_pattern():
    map = get_map()
    prior_maps = []
    for i in range(stop):
        perform_cycle(map)
        s = convert_to_string(map)
        if s in prior_maps:
            return prior_maps.index(s), i - prior_maps.index(s)
        prior_maps.append(s)


def get_map():
    result = []
    for line in get_lines():
        result.append(list(line))
    return result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


def perform_cycle(map):
    tilt_north(map)
    tilt_west(map)
    tilt_south(map)
    tilt_east(map)


def tilt_north(map):
    tilt(map, -1, 0)


def tilt_south(map):
    tilt(map, 1, 0)


def tilt_east(map):
    tilt(map, 0, 1)


def tilt_west(map):
    tilt(map, 0, -1)


def tilt(map, row_adjustment, col_adjustment):
    run_again = True
    while run_again:
        run_again = False
        for row in range(0, len(map)):
            for col in range(len(map[0])):
                neighbor_row, neighbor_col = row + row_adjustment, col + col_adjustment
                if is_valid_location(map, neighbor_row, neighbor_col) and map[row][col] == 'O' and map[neighbor_row][neighbor_col] == '.':
                    map[row][col], map[neighbor_row][neighbor_col] = '.', 'O'
                    run_again = True


def is_valid_location(map, row, col):
    if row < 0:
        return False
    if row >= len(map):
        return False
    if col < 0:
        return False
    if col >= len(map[0]):
        return False
    return True


def calculate_load(map):
    result = 0
    for i, row in enumerate(map):
        rocks = len([x for x in row if x == 'O'])
        distance = len(map) - i
        result += (rocks * distance)
    return result


def convert_to_string(map):
    rows = [''.join(row) for row in map]
    return ''.join(rows)


def print_map(map):
    for row in map:
        print(''.join(row))


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
