import functools
import re
import time


node_pattern = re.compile('([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)')


class Map:

    def __init__(self, current_position, network):
        self.current_position = current_position
        self.network = network

    def move(self, direction):
        current_node = self.network[self.current_position]
        next_position = current_node[0 if direction == 'L' else 1]
        self.current_position = next_position
        return self.current_position


def main():
    network = get_network()
    start_nodes = [x for x in network.keys() if x.endswith('A')]
    stop_node_step_numbers = []
    for a_node in start_nodes:
        map = Map(a_node, network)
        journey = find_cycle(map)
        cycle_start_item = journey[-1]
        pre_cycle_length = journey.index(cycle_start_item)
        cycle = journey[pre_cycle_length:]
        stop_node_step_numbers.append([i + pre_cycle_length for i, (x, _) in enumerate(cycle) if x.endswith('Z')][0])
    print(stop_node_step_numbers)
    print(lcm_list(stop_node_step_numbers))


def get_network():
    result = {}
    for line in get_lines():
        match = node_pattern.fullmatch(line)
        if match:
            result[match.group(1)] = (match.group(2), match.group(3))
    return result


def find_cycle(map: Map):
    move_generator = get_move_generator()
    journey = []
    while True:
        move_id, left_or_right = next(move_generator)
        journey_item = (map.current_position, move_id)
        journey.append(journey_item)
        if journey.count(journey_item) == 2:
            break
        map.move(left_or_right)
    return journey


def lcm_list(list):
    return functools.reduce(lcm, list)


def lcm(a, b):
    return a * (b // gcd(a, b))


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def get_move_generator():
    moves = next(get_lines())
    while True:
        for id, move in enumerate(moves):
            yield id, move


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
