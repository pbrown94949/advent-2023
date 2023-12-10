import collections
import re
import time

from typing import List

input_pattern = re.compile("(.+) ([0-9]+)")

hand_categories = ['high_card', 'one_pair', 'two_pair', 'three_of_a_kind', 'full_house', 'four_of_a_kind', 'five_of_a_kind']
card_labels = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
oaks = [None, None, 'one_pair', 'three_of_a_kind', 'four_of_a_kind', 'five_of_a_kind']


def categorize_hand(cards: str):
    jokers = cards.count('J')
    category = categorize_non_jokers([x for x in cards if x != 'J'])
    if jokers == 0:
        return category
    elif jokers == 5:
        return 'five_of_a_kind'
    elif category == 'four_of_a_kind':
        return 'five_of_a_kind'
    elif category == 'three_of_a_kind':
        return oaks[jokers + 3]
    elif category == 'two_pair':
        return 'full_house'
    elif category == 'one_pair':
        return oaks[jokers + 2]
    elif category == 'high_card':
        return oaks[jokers + 1]
    raise Exception('wtf')


def categorize_non_jokers(cards):
    if len(cards) == 0:
        return None
    temp = collections.defaultdict(int)
    for card in cards:
        temp[card] += 1
    counts = sorted([v for v in temp.values()], reverse=True)
    if counts[0] == 5:
        return 'five_of_a_kind'
    elif counts[0] == 4:
        return 'four_of_a_kind'
    elif counts[0:2] == [3, 2]:
        return 'full_house'
    elif counts[0] == 3:
        return 'three_of_a_kind'
    elif counts[0:2] == [2, 2]:
        return 'two_pair'
    elif counts[0] == 2:
        return 'one_pair'
    else:
        return 'high_card'


class Hand:

    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.category = categorize_hand(self.cards)

    def __repr__(self):
        return f"Hand({self.cards}, {self.category}, {self.bid})"

    def __lt__(self, other):
        self_category_value, other_category_value = hand_categories.index(self.category), hand_categories.index(other.category)
        if self_category_value != other_category_value:
            return self_category_value < other_category_value
        for self_card, other_card in zip(self.cards, other.cards):
            self_card_value, other_card_value = card_labels.index(self_card), card_labels.index(other_card)
            if self_card_value != other_card_value:
                return self_card_value < other_card_value
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
