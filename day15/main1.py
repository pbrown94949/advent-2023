import time


def main():
    commands = next(get_lines()).split(',')
    total = 0
    for command in commands:
        total += hash(command)
    print(total)


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


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
