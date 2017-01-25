# coding=utf-8
import sys
import random
import pprint
import pygame

import colors
import draw2d as draw


SQUARE = 0
DIAMOND = 1
LINES = 2
OVAL = 3
DONUT = 4
ALL_SHAPES = (SQUARE, DIAMOND, LINES, OVAL, DONUT)

SHAPE_LITERALS = {
    0: 'SQUARE',
    1: 'DIAMOND',
    2: 'LINES',
    3: 'OVAL',
    4: 'DONUT',
}


class Icon(object):
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def __eq__(self, other):
        return self.shape == other.shape and self.color == other.color

    def __repr__(self):
        return '[{},{}]'.format(SHAPE_LITERALS.get(self.shape), self.color)


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

        self.x_margin = int((self.win_w - self.board_w * (self.box_size + self.gap_size)) / 2)
        self.y_margin = int((self.win_h - self.board_h * (self.box_size + self.gap_size)) / 2)

        # Colors
        self.color_bg = colors.NAVY_BLUE
        self.color_light_bg = colors.GRAY
        self.color_box = colors.WHITE
        self.color_highlight = colors.YELLOW


class MemoryPuzzle(object):
    def __init__(self, config):
        # Configurations
        self.c = config

        # Initialize
        self.fps_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.c.win_w, self.c.win_h))
        self.surface.fill(self.c.color_bg)
        pygame.display.set_caption(u'Memory Puzzle')

    def run(self):
        pygame.init()
        mouse_x = 0
        mouse_y = 0

        board = self._gen_random_board()
        pprint.pprint(board)
        revealed = self._gen_revealed_box_data()

        # First select box
        first_selection = None

        while True:
            clicked = False
            self.surface.fill(self.c.color_bg)
            self._draw_board(board, revealed)
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT or (evt.type == pygame.KEYUP and evt.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = evt.pos
                elif evt.type == pygame.MOUSEBUTTONUP:
                    clicked = True

            i, j = self._get_box_by_xy(board, mouse_x, mouse_y)
            if i is not None and i is not None:
                if not revealed[i][j]:
                    self._draw_highlight_box(i, j)

                if not revealed[i][j] and clicked:
                    # self._reveal_animation(board, i, j)
                    revealed[i][j] = True

                    if first_selection is None:
                        first_selection = (i, j)
                    else:
                        icon0 = self._get_icon_shape_color(board, first_selection[0], first_selection[1])
                        icon1 = self._get_icon_shape_color(board, i, j)
                        if icon0 != icon1:
                            revealed[first_selection[0]][first_selection[1]] = False
                            revealed[i][j] = False
                        else:
                            # TODO check has_won
                            pass
                        first_selection = None


            pygame.display.update()
            self.fps_clock.tick(self.c.fps)

    def _gen_random_board(self):
        icons = []
        for shape in ALL_SHAPES:
            for color in colors.ALL_COLORS:
                if color == self.c.color_bg:
                    continue
                icons.append(Icon(shape, color))
        random.shuffle(icons)
        num_icons = int(self.c.board_w * self.c.board_h / 2)
        icons = icons[:num_icons] * 2
        random.shuffle(icons)

        offset = 0
        board = []
        for i in range(self.c.board_w):
            column = []
            for j in range(self.c.board_h):
                column.append(icons[offset])
                offset += 1
            board.append(column)
        return board

    def _gen_revealed_box_data(self):
        revealed = []
        for i in range(self.c.board_w):
            revealed.append([False] * self.c.board_h)
        return revealed

    def _get_box_by_xy(self, board, x, y):
        """
        获取鼠标坐标下的Icon坐标
        :param board:
        :param x:
        :param y:
        :return:
        """
        for i in range(self.c.board_w):
            for j in range(self.c.board_h):
                b_x, b_y = self._get_box_pos(i, j)
                rect = pygame.Rect(b_x, b_y, self.c.box_size, self.c.box_size)
                if rect.collidepoint(x, y):
                    return i, j
        return None, None

    def _get_box_pos(self, i, j):
        """
        根据Icon坐标获取屏幕坐标
        :param i:
        :param j:
        :return:
        """
        x = i * (self.c.box_size + self.c.gap_size) + self.c.x_margin
        y = j * (self.c.box_size + self.c.gap_size) + self.c.y_margin
        return x, y

    def _draw_icon(self, type_, color, i, j):
        """
        Commented use pygame.draw.
        Others are pygame.gfxdraw.
        TODO should unify

        :param type_:
        :param color:
        :param i:
        :param j:
        :return:
        """
        quarter = int(self.c.box_size * 0.25)
        half = int(self.c.box_size * 0.5)

        x, y = self._get_box_pos(i, j)
        if type_ == DONUT:
            # 5?
            # draw.circle(self.surface, color, (x + half, y + half), half - 5)
            draw.circle(self.surface, x+half, y+half, half - 5, color)
            draw.circle(self.surface, x+half, y+half, quarter - 5, self.c.color_bg)
        elif type_ == SQUARE:
            # draw.rect(self.surface, color, (x + quarter, y + quarter, self.c.box_size - half, self.c.box_size - half))
            draw.rect(
                self.surface, (x + quarter, y + quarter, self.c.box_size - half, self.c.box_size - half), color)
        elif type_ == DIAMOND:
            # draw.polygon(
            #     self.surface, color,
            #     [(x + half, y), (x + self.c.box_size - 1, y + half), (x + half, y + self.c.box_size - 1), (x, y + half)]
            # )
            draw.polygon(
                self.surface,
                [(x + half, y), (x + self.c.box_size - 1, y + half), (x + half, y + self.c.box_size - 1), (x, y + half)],
                color
            )
        elif type_ == LINES:
            for i in range(0, self.c.box_size, 4):
                # draw.line(self.surface, color, (x, y + i), (x + i, y))
                # draw.line(self.surface, color, (x + i, y + self.c.box_size - 1), (x + self.c.box_size - 1, y + i))
                draw.line(self.surface, x, y + i, x + i, y, color)
                draw.line(self.surface, x + i, y + self.c.box_size - 1, x + self.c.box_size - 1, y + i, color)
        elif type_ == OVAL:
            # draw.ellipse(self.surface, color, (x, y + quarter, self.c.box_size, half))
            draw.ellipse(self.surface, x + quarter + self.c.gap_size, y + quarter * 2, (self.c.box_size / 2), (half / 2), color)

        else:
            raise NotImplementedError('{} not supported'.format(type_))

    def _draw_board(self, main_board, revealed):
        for i in range(self.c.board_w):
            for j in range(self.c.board_h):
                x, y = self._get_box_pos(i, j)
                icon = main_board[i][j]
                if revealed and not revealed[i][j]:
                    draw.rect(self.surface, (x, y, self.c.box_size, self.c.box_size), self.c.color_box)
                else:
                    self._draw_icon(icon.shape, icon.color, i, j)

    def _draw_highlight_box(self, i, j):
        x, y = self._get_box_pos(i, j)
        draw.rect(self.surface, (x - 5, y - 5, self.c.box_size + 10, self.c.box_size + 10), self.c.color_highlight)

    def _draw_box_cover(self, i, j):
        pass

    def _get_icon_shape_color(self, board, i, j):
        icon = board[i][j]
        return icon.shape, icon.color

    def _reveal_animation(self, board, i, j):
        pass

    def _has_won(self, revealed):
        for col in revealed:
            if False in col:
                return False
        return True


if __name__ == '__main__':
    app = MemoryPuzzle(_Config())
    app.run()
