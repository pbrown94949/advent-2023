import re
import time

card_pattern = re.compile("Card[ ]+([1-9][0-9]*): ([0-9 ]+)\|([0-9 ]+)")
number_pattern = re.compile("[1-9][0-9]*")

def main():
    cards = {}
    for line in get_lines():
        match = card_pattern.fullmatch(line)
        card_id = int(match.group(1))
        winning_number_list = set(number_pattern.findall(match.group(2)))
        guessed_number_list = set(number_pattern.findall(match.group(3)))
        winning_guesses_count = len(winning_number_list & guessed_number_list)
        cards[card_id] = {
            'winning_guesses_count': winning_guesses_count,
            'count': 1
        }
    for card_id, card in cards.items():
        winning_guesses_count = card['winning_guesses_count']
        card_count = card['count']
        for i in range(winning_guesses_count):
            cards[card_id + i + 1]['count'] += card_count
    total = 0
    for card in cards.values():
        total += card['count']
    print(total)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
