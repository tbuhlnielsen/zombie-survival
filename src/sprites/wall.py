
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import settings
import sprites.template

# ==============================================================================

class Wall(sprites.template.Entity):

    def __init__(self, x, y, img):
        """Initialise a Wall at tile location (x, y)."""
        super().__init__(x, y, img)
        
        self.image = pg.transform.scale(self.original_image, settings.TILE_AREA)

        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y
