
"""Zombie survival game

core.ui.camera - Class for scrolling around different parts of a map as they
                 are explored.
"""

import pygame as pg

from constants.settings import Window


class Camera:
    """Follows the player around a map."""

    def __init__(self, width, height):
        """TO DO: explain."""
        self.view_area = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """TO DO: explain."""
        return entity.rect.move(self.view_area.topleft)

    def apply_rect(self, rect):
        """TO DO: explain."""
        return rect.move(self.view_area.topleft)

    def update(self, target):
        """TO DO: explain."""
        x = -target.rect.centerx + Window["width"] // 2
        y = -target.rect.centery + Window["height"] // 2

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(Window["width"] - self.width, x) # right

        y = min(0, y) # top
        y = max(Window["height"] - self.height, y) # bottom

        self.view_area = pg.Rect(x, y, self.width, self.height)
