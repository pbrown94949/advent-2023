import time

boxes = [[] for _ in range(256)]


def main():
    commands = next(get_lines()).split(',')
    for command in commands:
        if '=' in command:
            lens, focal_length = command.split('=')
            add_lens(lens, int(focal_length))
        else:
            lens = command[:-1]
            remove_lens(lens)
    focusing_power = calculate_focusing_power()
    print(focusing_power)


def get_lines():
    with open('input.txt') as file:
        for line in file:
            yield line.strip()


def hash(str):
    result = 0
    for c in list(str):
        result += ord(c)
        result *= 17
        result = result % 256
    return result


def add_lens(lens, focal_length):
    box = hash(lens)
    idx = find_lens(boxes[box], lens)
    if idx is not None:
        boxes[box][idx][1] = focal_length
    else:
        boxes[box].append([lens, focal_length])


def remove_lens(lens):
    box = hash(lens)
    idx = find_lens(boxes[box], lens)
    if idx is not None:
        del boxes[box][idx]


def find_lens(box, lens):
    for idx, item in enumerate(box):
        if item[0] == lens:
            return idx
    return None


def calculate_focusing_power():
    result = 0
    for i, box in enumerate(boxes, start=1):
        for j, lens in enumerate(box, start=1):
            focal_length = lens[1]
            result += (i * j * focal_length)
    return result


def print_boxes():
    for i, box in enumerate(boxes):
        if len(box) > 0:
            print(i, box)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
