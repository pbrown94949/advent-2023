import re
import time

game_pattern = re.compile("Game ([1-9][0-9]*): .*")
color_pattern = re.compile("([1-9][0-9]*) (blue|red|green)")


def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            minimums = get_minimum_cubes(line)
            power = get_power(minimums)
            total += power
    print(total)


def get_minimum_cubes(line):
    minimums = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    for count, color in color_pattern.findall(line):
        count = int(count)
        if minimums[color] < count:
            minimums[color] = count
    return minimums


def get_power(minimums):
    result = 1
    for v in minimums.values():
        result *= v
    return result


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
