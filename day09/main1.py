import re
import time

from typing import List

integers_pattern = re.compile('-?[0-9]+')

def main():
    total = 0
    for sequence in read_sequences():
        next_value = predicate_next_value(sequence)
        total += next_value
    print(total)


def read_sequences():
    for line in get_lines():
        yield find_all_integers(line)


def predicate_next_value(sequence: List[int]):
    reduction = reduce_sequence(sequence)
    return sum(lst[-1] for lst in reduction)


def reduce_sequence(sequence: List[int]) -> List[List[int]]:
    result = [sequence[:]]
    while not all_zeroes(result[-1]):
        result.append(calculate_differences(result[-1]))
    return result


def calculate_differences(sequence: List[int]) -> List[int]:
    result = []
    for i in range(1, len(sequence)):        
        result.append(sequence[i] - sequence[i - 1])
    return result


def all_zeroes(sequence):
    for x in sequence:
        if x != 0:
            return False
    return True


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
