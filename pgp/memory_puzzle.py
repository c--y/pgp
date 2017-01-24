# coding=utf-8
import sys
import random
import pygame

import colors


SQUARE = 0
DIAMOND = 1
LINES = 2
OVAL = 3
DONUT = 4
ALL_SHAPES = (SQUARE, DIAMOND, LINES, OVAL, DONUT)


class Icon(object):
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color


class _Config(object):
    def __init__(self):
        self.fps = 30
        self.win_w = 640
        self.win_h = 480
        self.board_w = 10
        self.board_h = 7
        # Size of box in pixels
        self.box_size = 40
        # Size of gap between boxes in pixels
        self.gap_size = 10

        # Colors
        self.color_bg = colors.NAVY_BLUE
        self.color_light_bg = colors.GRAY
        self.color_box = colors.WHITE
        self.color_high_light = colors.BLUE


class MemoryPuzzle(object):
    def __init__(self, config):
        # Configurations
        self.config = config

        # Initialize
        self.fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.config.win_w, self.config.win_h))
        self.surface.fill(self.config.color_bg)
        pygame.display.set_caption(u'Memory Puzzle')

    def run(self):
        pygame.init()
        mouse_x = 0
        mouse_y = 0

        board = self._gen_random_board()

        # First select box
        first_selection = None

        while True:
            self.surface.fill(self.config.color_bg)
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT or (evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                print evt

            pygame.display.update()

    def _gen_random_board(self):
        icons = []
        for shape in ALL_SHAPES:
            for color in colors.ALL_COLORS:
                icons.append(Icon(shape, color))
        random.shuffle(icons)


        return []

    def _gen_revealed_box_data(self):
        return []

    def _get_box_by_xy(self, x, y):
        return None

    def _draw_icons(self, type_, color, x, y):
        if type_ == DONUT:
            pass
        elif type_ == SQUARE:
            pass
        elif type_ == DIAMOND:
            pass
        elif type_ == LINES:
            pass
        else:
            raise NotImplementedError('{} not supported'.format(type_))


if __name__ == '__main__':
    app = MemoryPuzzle(_Config())
    app.run()
