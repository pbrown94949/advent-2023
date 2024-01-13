from typing import Set

import main2

import pygame


screen_color = (0, 0, 0)
yellow = (255, 255, 0)
purple = (255, 0, 255)


def init():
    global WIN
    pygame.init()
    WIDTH, HEIGHT = 900, 900
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def add_line(line_segment: main2.LineSegment, color):
    pygame.draw.line(WIN, color, (line_segment.endpoints[0].col, line_segment.endpoints[0].row), (line_segment.endpoints[1].col, line_segment.endpoints[1].row), 2)
    pygame.display.update()


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def display(line_segment_collection: main2.LineSegmentCollection, u_shapes: Set[main2.LineSegment]):
    min_row_number = min([x.row for x in line_segment_collection.get_by_orientation(main2.Orientation.HORIZONTAL)])
    min_col_number = min([x.col for x in line_segment_collection.get_by_orientation(main2.Orientation.VERTICAL)])
    init()
    for i in range(len(line_segment_collection)):
        ls = line_segment_collection[i]
        ls = ls.translate_to_zero_based(min_row_number - 20, min_col_number - 20)
        ls = ls * 2
        add_line(ls, yellow)
    for ls in u_shapes:
        ls = ls.translate_to_zero_based(min_row_number - 20, min_col_number - 20)
        ls = ls * 2
        add_line(ls, purple)
    wait()
