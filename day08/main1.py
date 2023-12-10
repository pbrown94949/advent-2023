import re
import time


node_pattern = re.compile('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)')


def main():
    generator = get_move_generator()
    network = get_network()
    current_position = 'AAA'
    total = 0
    while current_position != 'ZZZ':
        next_move = next(generator)
        current_position = network[current_position][0 if next_move == 'L' else 1]
        total += 1
    print(total)


def get_move_generator():
    moves = next(get_lines())
    while True:
        for x in moves:
            yield x


def get_network():
    result = {}
    for line in get_lines():
        match = node_pattern.fullmatch(line)
        if match:
            result[match.group(1)] = (match.group(2), match.group(3))
    return result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
