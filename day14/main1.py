import time


def main():
    map = get_map()
    tilt_north(map)
    load = calculate_load(map)
    print(load)


def get_map():
    result = []
    for line in get_lines():
        result.append(list(line))
    return result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


def tilt_north(map):
    run_again = True
    while run_again:
        run_again = False
        for row in range(1, len(map)):
            for col in range(len(map[0])):
                if map[row][col] == 'O' and map[row - 1][col] == '.':
                    map[row][col], map[row - 1][col] = '.', 'O'
                    run_again = True


def calculate_load(map):
    result = 0
    for i, row in enumerate(map):
        rocks = len([x for x in row if x == 'O'])
        distance = len(map) - i
        result += (rocks * distance)
    return result


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
