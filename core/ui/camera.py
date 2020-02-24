
"""Zombie survival game

core.ui.camera - Class for scrolling around different parts of a map as they
                 are explored.

TO DO: add documentation.
"""

import pygame as pg

from constants.settings import *


class Camera:
    """Follows the player around a map."""

    def __init__(self, width, height):
        self.view_area = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.view_area.topleft)

    def apply_rect(self, rect):
        return rect.move(self.view_area.topleft)

    def update(self, target):
        x = -target.rect.centerx + WIDTH // 2
        y = -target.rect.centery + HEIGHT // 2

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(WIDTH - self.width, x) # right

        y = min(0, y) # top
        y = max(HEIGHT - self.height, y) # bottom

        self.view_area = pg.Rect(x, y, self.width, self.height)
