"""
This is only a partial answer. 
Looking at the input as a flowchart in mermaid I can see the following: 
rx will be triggered when dr is.
dr will be triggered when all mp, qt, qb, and ng are triggered. 

I used this code to find the lengths of the cycles for the important nodes, shown here: 
mp: 3917
qt: 4007
qb: 4027
ng: 3919

Then the answer was just the LCD of these 4 numbers which I got from Wolfram alpha.

Kind of cheap.
"""

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
        self.last_pulse: Pulse = None
        self.receivers = []

    def receive(self, message: Message):
        self.last_pulse = message.pulse
        return []


class Network:

    def __init__(self, modules):
        self.modules = modules
        self.high_pulses_sent = self.low_pulses_sent = 0
        self.clicks = 0

    def push_button(self):
        self.clicks += 1
        queue = collections.deque()
        queue.append(Message('button', 'broadcaster', Pulse.LOW))
        while queue:
            message: Message = queue.popleft()
            if message.receiver == 'ng' and message.pulse == Pulse.LOW:
                print(message, self.clicks)
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


def process1():
    modules = build_modules()
    labels = {}
    for m in modules:
        if isinstance(m, FlipFlop):
            type = 'ff-'
        elif isinstance(m, Conjunction):
            type = 'con-'
        else:
            type = ''
        labels[m.name] = f"{type}{m.name}"
    for m in modules:        
        for r in m.receivers:
            print(f"{labels[m.name]} --> {labels[r]}")


def process():
    network = build_network()
    while True:
        network.push_button()


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
    print(len(result))
    module_names = set([x.name for x in result])
    # include receivers who are not senders
    for receiver in receiver_to_senders:
        if receiver not in module_names:
            result.append(NoopModule(receiver))
            module_names.add(receiver)
    print(len(result))
    queue = collections.deque(['rx'])
    can_get_to_rx = set()
    while queue:
        receiver = queue.popleft()
        if receiver not in can_get_to_rx:
            can_get_to_rx.add(receiver)
            senders = receiver_to_senders[receiver]
            for s in senders:
                queue.append(s)
    result = [x for x in result if x.name in can_get_to_rx]
    print(len(result))
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
