
"""Zombie survival game

core.sprite
"""

import pygame as pg

from core.tools.collisions import axis_collide

from constants.settings import *


class Character(pg.sprite.Sprite):
    """Base class for a character that can move, rotate, and collide with
    other game objects.
    """

    def __init__(self, game, x, y, img, max_speed, max_spin_rate):
        """Set up the mechanics and appearance of a Character."""

        self._layer = CHARACTER_LAYER
        super().__init__()

        self.game = game

        # mechanics
        self.position = pg.math.Vector2(x, y)

        self.max_speed = max_speed # pixels per second
        self.velocity = pg.math.Vector2(0, 0) # set components to +- max_speed

        self.acceleration = pg.math.Vector2(0, 0)

        self.max_spin_rate = max_spin_rate # degrees per second
        self.rotate_speed = 0 # set to +- max_spin_rate
        self.rotation = 0 # degrees

        # appearance
        self.original_image = img # for applying transformations to
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # collision rect
        s = int(TILE_SIZE * 0.75)
        self.hit_rect = pg.Rect(0, 0, s, s)
        self.hit_rect.center = (x, y)

        # other
        self.max_health = 100
        self.health = self.max_health

    def rotate_image(self):
        """Updates self.image by rotating self.original_image."""
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def check_for_collide(self):
        """Updates a Character's position if it collides with an obstacle."""
        self.hit_rect.centerx = self.position.x
        axis_collide(self, self.game.get_scene().obstacles, "x")

        self.hit_rect.centery = self.position.y
        axis_collide(self, self.game.get_scene().obstacles, "y")

        self.rect.center = self.hit_rect.center

    def is_injured(self):
        """True iff a Character's health has decreased."""
        return self.health < self.max_health
