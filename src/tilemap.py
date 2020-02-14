
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import os
import pygame as pg

import settings

# ==============================================================================

MAPS_DIR = os.path.join(os.path.dirname(__file__), "maps")

class Map:
    """Stores the initial locations of objects in a scene."""

    def __init__(self, file_name):
        """Read data from file_name (a txt file in MAPS_DIR)."""
        full_name = os.path.join(MAPS_DIR, file_name)

        self.data = []
        with open(full_name, "r") as f:
            for line in f:
                self.data.append(line.strip())

        self.nx_tiles = len(self.data[0])
        self.ny_tiles = len(self.data)

        self.width = self.nx_tiles * settings.TILE_SIZE
        self.height = self.ny_tiles * settings.TILE_SIZE

# ==============================================================================

class Camera:
    """Follows the player around a map."""

    def __init__(self, width, height):
        self.view_area = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.view_area.topleft)

    def update(self, target):
        x = -target.rect.centerx + settings.WINDOW_WIDTH // 2
        y = -target.rect.centery + settings.WINDOW_HEIGHT // 2

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(settings.WINDOW_WIDTH - self.width, x) # right

        y = min(0, y) # top
        y = max(settings.WINDOW_HEIGHT - self.height, y) # bottom

        self.view_area = pg.Rect(x, y, self.width, self.height)
