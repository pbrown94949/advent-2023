import re
import time

number_words = ['one', 'two', 'three', 'four',
                'five', 'six', 'seven', 'eight', 'nine']
digits = [str(x) for x in range(1, 10)]

forward_pattern = '|'.join(number_words + digits)
backward_pattern = forward_pattern[::-1]

forward_pattern = re.compile(forward_pattern)
backward_pattern = re.compile(backward_pattern)


def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            first = forward_pattern.search(line).group(0)
            last = backward_pattern.search(line[::-1]).group(0)[::-1]
            first, last = get_value(first), get_value(last)
            calibration_value = first * 10 + last
            total += calibration_value
    print(total)


def get_value(string):
    if len(string) == 1:
        return int(string)
    return number_words.index(string) + 1


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
