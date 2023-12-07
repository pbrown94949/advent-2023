import re
import time

card_pattern = re.compile("Card[ ]+[1-9][0-9]*: ([0-9 ]+)\|([0-9 ]+)")
number_pattern = re.compile("[1-9][0-9]*")


def main():
    total = 0
    for line in get_lines():
        match = card_pattern.fullmatch(line)
        winning_numbers = set(number_pattern.findall(match.group(1)))
        my_numbers = set(number_pattern.findall(match.group(2)))
        my_winning_numbers = len(winning_numbers & my_numbers)
        card_score = 2 ** (my_winning_numbers - 1) if my_winning_numbers else 0
        total += card_score
    print(total)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
