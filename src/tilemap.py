
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).

TO DO: rename to mapgen.py?
"""

import os
import pygame as pg

import pytmx

import settings

# ==============================================================================

(ROOT_DIR, _) = os.path.split(os.path.dirname(__file__))
MAPS_DIR = os.path.join(ROOT_DIR, "data", "maps")

class Map:
    """Stores the initial locations of a Scene's objects."""

    def __init__(self, file_name):
        """Read data from file_name (a txt file in MAPS_DIR)."""
        full_name = os.path.join(MAPS_DIR, "text", file_name)

        self.data = []
        with open(full_name, "r") as f:
            for line in f:
                self.data.append(line.strip())

        self.nx_tiles = len(self.data[0])
        self.ny_tiles = len(self.data)

        self.width = self.nx_tiles * settings.TILE_SIZE
        self.height = self.ny_tiles * settings.TILE_SIZE

# ---------------------------------------

class TiledMap:
    """ """

    def __init__(self, file_name):
        """Read data from file_name (a tmx file in MAPS_DIR)."""
        full_name = os.path.join(MAPS_DIR, "tmx", file_name)

        self.data = pytmx.load_pygame(full_name, pixelalpha=True)

        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.area = (self.width, self.height)

    def render(self, surf):
        """Draw the tiles of self.data onto surf (a pygame surface)."""
        # shorten command
        ti = self.data.get_tile_image_by_gid

        # draw tiles layer by layer
        for layer in self.data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surf.blit(tile, (x * self.data.tilewidth,
                                         y * self.data.tileheight))

    def make(self):
        """ """
        surf = pg.Surface(self.area)
        self.render(surf)

        return surf

# ==============================================================================

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
        x = -target.rect.centerx + settings.WINDOW_WIDTH // 2
        y = -target.rect.centery + settings.WINDOW_HEIGHT // 2

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(settings.WINDOW_WIDTH - self.width, x) # right

        y = min(0, y) # top
        y = max(settings.WINDOW_HEIGHT - self.height, y) # bottom

        self.view_area = pg.Rect(x, y, self.width, self.height)
