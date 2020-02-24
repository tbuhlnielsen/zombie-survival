
"""Zombie survival game

core.sprites.world - Classes representing objects that are part of the
                     "game world".
"""

import pygame as pg

from constants.settings import OBSTACLE_LAYER


class Obstacle(pg.sprite.Sprite):
    """Blocks/stops other game objects."""

    def __init__(self, game, x, y, w, h):
        """Sets up the location and size of an Obstacle."""
        self._layer = OBSTACLE_LAYER
        super().__init__()

        self.game = game
        self.game.get_scene().obstacles.add(self)

        self.x = x
        self.y = y

        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
