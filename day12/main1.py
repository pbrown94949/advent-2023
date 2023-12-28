import itertools
import re
import time

broken_springs_pattern = re.compile("#+")
integers_pattern = re.compile('[0-9]+')


def main():
    total = 0
    for line in get_lines():
        record1, record2 = parse_line(line)
        total += count_possible_solutions(record1, record2)
    print(total)


def parse_line(line: str):
    record1, record2 = line.split()
    record2 = tuple(int(x) for x in find_all_integers(record2))
    return record1, record2


def count_possible_solutions(record1, record2):
    record1_damaged_spring_count = record1.count("#")
    record1_unknown_status_indexes = [i for i, spring in enumerate(record1) if spring == '?']
    record2_damaged_spring_count = sum(record2)
    result = 0
    for indexes in itertools.combinations(record1_unknown_status_indexes, record2_damaged_spring_count - record1_damaged_spring_count):
        record1a = build_revised_record1(record1, indexes)
        if records_match(record1a, record2):
            result += 1
    return result


def build_revised_record1(record1, indexes):
    temp = list(record1)
    for index in indexes:
        temp[index] = "#"
    return ''.join(temp)


def records_match(record1, record2):
    return tuple(len(x) for x in broken_springs_pattern.findall(record1)) == record2


def find_all_integers(line):
    return [int(x) for x in integers_pattern.findall(line)]


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
