
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import settings

# ==============================================================================

class Wall(pg.sprite.Sprite):

    def __init__(self, x, y):
        """Initialise a Wall at tile location (x, y)."""
        super().__init__()

        self.original_image = fx.load_image("tile_green.png")
        self.image = pg.transform.scale(self.original_image, settings.TILE_AREA)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE
