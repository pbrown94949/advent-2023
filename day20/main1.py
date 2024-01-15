import argparse
import collections
import re
import time

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()

comma_delimited_pattern = re.compile("([^ ,]+)")

module_pattern = re.compile("""
                            (?P<type>[%&]?)         
                            (?P<name>[^ ]+)          # module name
                            [ ]->[ ]                 # arrow
                            (?P<destinations>.*)     # destinations
                            """, re.VERBOSE)


class Pulse(Enum):
    LOW = 'low'
    HIGH = 'high'


@dataclass(frozen=True)
class Message():
    sender: str
    receiver: str
    pulse: Pulse


class FlipFlop:

    def __init__(self, name, receivers):
        self.name = name
        self.off = True
        self.receivers = receivers

    def receive(self, message: Message) -> List[Message]:
        if message.pulse == Pulse.HIGH:
            return []
        pulse = Pulse.HIGH if self.off else Pulse.LOW
        self.off = not self.off
        return [Message(self.name, receiver, pulse) for receiver in self.receivers]


class Conjunction:

    def __init__(self, name, senders, receivers):
        self.name = name
        self.inputs: Dict[str, Pulse] = {x: Pulse.LOW for x in senders}
        self.receivers = receivers

    def receive(self, message: Message) -> List[Message]:
        self.inputs[message.sender] = message.pulse
        pulse = Pulse.LOW if all([x == Pulse.HIGH for x in self.inputs.values()]) else Pulse.HIGH
        return [Message(self.name, receiver, pulse) for receiver in self.receivers]


class Broadcaster:

    def __init__(self, name, receivers):
        self.name = name
        self.receivers = receivers

    def receive(self, message: Message) -> List[Message]:
        return [Message(self.name, receiver, message.pulse) for receiver in self.receivers]


class NoopModule:

    def __init__(self, name):
        self.name = name

    def receive(self, message: Message):
        return []


class Network:

    def __init__(self, modules):
        self.modules = modules
        self.high_pulses_sent = self.low_pulses_sent = 0

    def push_button(self):
        queue = collections.deque()
        queue.append(Message('button', 'broadcaster', Pulse.LOW))
        while queue:
            message: Message = queue.popleft()
            self.high_pulses_sent += (1 if message.pulse == Pulse.HIGH else 0)
            self.low_pulses_sent += (1 if message.pulse == Pulse.LOW else 0)
            # print(f"{message.sender} -> {message.pulse.value} -> {message.receiver}")
            recipient = [x for x in self.modules if x.name == message.receiver][0]
            for m in recipient.receive(message):
                queue.append(m)


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():
    network = build_network()
    for _ in range(1000):
        network.push_button()
    result = network.high_pulses_sent * network.low_pulses_sent
    print(result)


def build_network():
    return Network(build_modules())


def build_modules():
    result = []
    sender_to_receivers, receiver_to_senders = get_sender_receiver_mapping()
    for module_type, module_name, _ in get_modules():
        if module_type == '%':
            module = FlipFlop(module_name, sender_to_receivers[module_name])
        elif module_type == '&':
            module = Conjunction(module_name, receiver_to_senders[module_name], sender_to_receivers[module_name])
        elif module_name == 'broadcaster':
            module = Broadcaster(module_name, sender_to_receivers[module_name])
        else:
            raise Exception('wtf')
        result.append(module)
    module_names = set([x.name for x in result])
    for receiver in receiver_to_senders:
        if receiver not in module_names:
            result.append(NoopModule(receiver))
            module_names.add(receiver)
    return result


def get_sender_receiver_mapping():
    source_to_dest, dest_to_source = collections.defaultdict(list), collections.defaultdict(list)
    for _, module_name, destinations in get_modules():
        for destination in destinations:
            source_to_dest[module_name].append(destination)
            dest_to_source[destination].append(module_name)
    return source_to_dest, dest_to_source


def get_modules():
    for line in get_lines():
        match = module_pattern.fullmatch(line)
        module_type = match.group('type')
        module_name = match.group('name')
        destinations = comma_delimited_pattern.findall(match.group('destinations'))
        yield module_type, module_name, destinations


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
