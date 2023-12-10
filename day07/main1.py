import collections
import re
import time

from dataclasses import dataclass
from typing import List

input_pattern = re.compile("(.+) ([0-9]+)")

hand_types = ['high_card', 'one_pair', 'two_pair', 'three_of_a_kind', 'full_house', 'four_of_a_kind', 'five_of_a_kind']
card_labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


def get_hand_type(cards):
    cardinality = len(set(list(cards)))
    if cardinality == 1:
        return 'five_of_a_kind'
    elif cardinality == 4:
        return 'one_pair'
    elif cardinality == 5:
        return 'high_card'
    temp = collections.defaultdict(int)
    for card in list(cards):
        temp[card] += 1
    max_occurrence = max(temp.values())
    if cardinality == 2:
        return 'four_of_a_kind' if max_occurrence == 4 else 'full_house'
    if cardinality == 3:
        return 'three_of_a_kind' if max_occurrence == 3 else 'two_pair'
    raise Exception('wtf')


class Hand:

    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.type = get_hand_type(self.cards)

    def __repr__(self):
        return f"Hand({self.cards}, {self.type}, {self.bid})"

    def __lt__(self, other):
        a, b = hand_types.index(self.type), hand_types.index(other.type)
        if a != b:
            return a < b
        for a, b in zip(self.cards, other.cards):
            a, b = card_labels.index(a), card_labels.index(b)
            if a != b:
                return a < b
        return False


def main():
    hands: List[Hand] = []
    for line in get_lines():
        match = input_pattern.fullmatch(line)
        cards, bid = match.group(1), int(match.group(2))
        hands.append(Hand(cards, bid))
    hands.sort()
    total = 0
    for rank, hand in enumerate(hands, start=1):
        total += (rank * hand.bid)
    print(total)



def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
