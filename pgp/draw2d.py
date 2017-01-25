# coding=utf-8
from pygame import gfxdraw


def circle(surface, x, y, r, color):
    gfxdraw.aacircle(surface, x, y, r, color)
    gfxdraw.filled_circle(surface, x, y, r, color)


def polygon(surface, points, color):
    gfxdraw.aapolygon(surface, points, color)
    gfxdraw.filled_polygon(surface, points, color)


def line(surface, x1, y1, x2, y2, color):
    gfxdraw.line(surface, x1, y1, x2, y2, color)


def rect(surface, rect, color):
    gfxdraw.rectangle(surface, rect, color)
    gfxdraw.box(surface, rect, color)


def ellipse(surface, x, y, rx, ry, color):
    gfxdraw.aaellipse(surface, x, y, rx, ry, color)
    gfxdraw.filled_ellipse(surface, x, y, rx, ry, color)