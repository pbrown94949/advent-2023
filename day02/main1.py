import re
import time

game_pattern = re.compile("Game ([1-9][0-9]*): .*")
color_pattern = re.compile("([1-9][0-9]*) (blue|red|green)")

max_cubes = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            game_id = int(game_pattern.match(line).group(1))
            if was_possible(line):
                total += game_id
    print(total)


def was_possible(line):
    for count, color in color_pattern.findall(line):
        if int(count) > max_cubes[color]:
            return False
    return True


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
