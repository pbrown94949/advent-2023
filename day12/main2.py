import collections
import itertools
import re
import time

integers_pattern = re.compile('[0-9]+')


def find_all_integers(line):
    return [int(x) for x in integers_pattern.findall(line)]


def main():
    total = 0
    for i, line in enumerate(get_lines(), start=1):
        record1, record2 = parse_line(line)
        record1, record2 = quintuple(record1, record2)
        subtotal = count_solutions(record1, record2)
        total += subtotal
    print(total)


def parse_line(line: str):
    record1, record2 = line.split()
    record2 = tuple([int(x) for x in find_all_integers(record2)])
    return record1, record2


def quintuple(record1, record2):
    return '?'.join(itertools.repeat(record1, 5)), record2 * 5


def count_solutions(record1, record2):
    record1_min_hashes = record1.count('#')
    record1_max_hashes = record1_min_hashes + record1.count('?')
    record2_hashes = sum(record2)
    if record2_hashes < record1_min_hashes or record2_hashes > record1_max_hashes:
        return 0
    record2_left, record2_mid, record2_right = split_record2(record2)
    if record2_mid is None:
        return 0 if '#' in record1 else 1
    subsequence_locations = locate_sequences(record1, record2_mid)
    if len(subsequence_locations) == 0:
        return 0
    result = 0
    subsequence_location_counts = collections.defaultdict(int)
    for subsequence_location in subsequence_locations:
        subsequence_location_counts[subsequence_location] += 1
    for (start, stop), count in subsequence_location_counts.items():
        record1_left, record1_right = record1[:start], record1[stop:]
        solutions = count_solutions_shortest_first([(record1_left, record2_left), (record1_right, record2_right)])
        result += (count * solutions)
    return result


def count_solutions_shortest_first(pairs):
    pairs.sort(key=lambda x: len(x[0]))
    result = 1
    for pair in pairs:
        solutions = count_solutions(*pair)
        if solutions == 0:
            return 0
        result *= solutions
    return result


def split_record2(record2):
    if len(record2) == 0:
        return [], None, []
    midpoint = len(record2) // 2
    return record2[:midpoint], record2[midpoint], record2[midpoint+1:]


def locate_sequences(string, hash_count):
    if len(string) < hash_count:
        return []
    if len(string) == hash_count:
        if is_valid_hash_sequence(string, False, False):
            return [(0, len(string))]
    result = []
    substring_size = hash_count + 2
    for i in range(len(string)):
        start, stop = i, i + substring_size
        substring = string[start:stop]
        if len(substring) < substring_size:
            break
        if is_valid_hash_sequence(substring):
            result.append((start, stop))
    # Special handling for the start and end of the string
    substring_size = hash_count + 1
    for start, stop, require_leading_dot, require_trailing_dot in [
        (0, substring_size, False, True),
        (len(string) - substring_size, len(string), True, False)
    ]:
        substring = string[start:stop]
        if is_valid_hash_sequence(substring, require_leading_dot, require_trailing_dot):
            result.append((start, stop))
    return result


def is_valid_hash_sequence(string, require_leading_dot=True, require_trailing_dot=True):
    if not require_leading_dot and not require_trailing_dot:
        return is_hashes_or_queries(string)
    if require_leading_dot:
        if string[0] == '#':
            return False
        return is_valid_hash_sequence(string[1:], False, require_trailing_dot)
    if require_trailing_dot:
        if string[-1] == '#':
            return False
        return is_valid_hash_sequence(string[:-1], False, False)


def is_hashes_or_queries(string):
    for char in string:
        if char not in ['#', '?']:
            return False
    return True


def split_by_range(string, start, end):
    return string[:start], string[end:]


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
