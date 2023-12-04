import time

ascii_zero = ord('0')
ascii_nine = ord('9')


def main():
    total = 0
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            first, last = get_first_and_last_digits(line)
            calibration_value = first * 10 + last
            total += calibration_value
    print(total)


def get_first_and_last_digits(line):
    temp = [int(x) for x in list(line) if is_digit(x)]
    return temp[0], temp[-1]


def is_digit(char):
    return ord(char) >= ascii_zero and ord(char) <= ascii_nine


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
