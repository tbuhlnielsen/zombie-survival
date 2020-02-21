
"""Zombie survival game

core.ui.tilemap - Class for getting data from tmx files.
"""

import pytmx
import pygame as pg

from os import path

from constants.paths import MAPS_DIR
from constants.settings import Tile, Window


class TiledMap:
    """A map created with the Tiled map editor."""

    def __init__(self, file_name):
        """Read data from MAPS_DIR/file_name."""
        full_name = path.join(MAPS_DIR, file_name) + ".tmx"

        # parts of map are transparent
        self.data = pytmx.load_pygame(full_name, pixelalpha=True)

        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.area = (self.width, self.height)

    def render(self, surf):
        """Draw the tiles of self.data onto surf (a pygame surface)."""
        for layer in self.data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.data.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * self.data.tilewidth,
                                         y * self.data.tileheight))

    def make(self):
        """TO DO: explain."""
        surf = pg.Surface(self.area)
        self.render(surf)

        return surf
