import re
import time

symbol_pattern = re.compile('[^0-9\.]')
number_pattern = re.compile('([1-9][0-9]*)')


def main():
    total = 0
    symbols = get_symbol_locations()
    for val, row, col_start, col_end in get_numbers():
        neighbors = get_neighbors(row, col_start, col_end)
        if not symbols.isdisjoint(neighbors):
            total += val
    print(total)


def get_symbol_locations():
    result = set()
    for row, line in enumerate(get_lines()):
        for col, char in enumerate(list(line)):
            if is_symbol(char):
                result.add((row, col))
    return result


def is_symbol(char):
    return symbol_pattern.fullmatch(char) != None


def get_numbers():
    for row, line in enumerate(get_lines()):
        for match in number_pattern.finditer(line):
            yield int(match.group(1)), row, match.start(1), match.end(1) - 1


def get_neighbors(row, col_start, col_end):
    result = set()
    for r in range(row - 1, row + 2):
        for c in range(col_start - 1, col_end + 2):
            if r != row or c < col_start or c > col_end:
                result.add((r, c))
    return result


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
