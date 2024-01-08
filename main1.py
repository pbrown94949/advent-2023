import argparse
import time

argparser = argparse.ArgumentParser()
argparser.add_argument('file')

start_time = time.time()


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()


def process():
    pass


def get_lines():
    with open(args.file) as file:
        for line in file:
            yield line.strip()


def wrapup():
    pass


if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % int(time.time() - start_time))
