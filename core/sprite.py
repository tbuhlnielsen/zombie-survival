
"""Zombie survival game

core.sprite - Base class for a character that can move, rotate, and collide with
              other game objects.
"""

import pygame as pg

from constants.settings import *


# shorten name
vec = pg.math.Vector2


class Character(pg.sprite.Sprite):
    """Base class for a character that can move, rotate, and collide with
    other game objects.
    """

    def __init__(self, game, x, y, image, max_speed):
        """Set up the mechanics and appearance of a Character."""
        # drawing layer
        self._layer = CHARACTER_LAYER
        super().__init__()

        self.game = game

        # mechanics
        self.position = vec(x, y)

        self.max_speed = max_speed # pixels per second
        self.velocity = vec(0, 0) # set components to +- max_speed

        self.acceleration = vec(0, 0)

        self.rotate_speed = 0 # set to +- MAX_SPIN_RATE
        self.rotation = 0 # degrees

        # appearance
        self.original_image = image # for applying transformations to
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # collision rect - slightly smaller than image rect
        s = int(TILE_SIZE * 0.75)
        self.hit_rect = pg.Rect(0, 0, s, s)
        self.hit_rect.center = (x, y)

        # health
        self._health = MAX_HEALTH

    def rotate_image(self):
        """Updates a character's image by rotating its original image."""
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_health(self):
        """Returns the value of a character's health."""
        return self._health

    def increase_health(self, amount):
        """Increases the health of a character by amount (can be negative)."""
        self._health = min(MAX_HEALTH, self._health + amount)

    def is_injured(self):
        """True iff a character's health has decreased."""
        return self._health < MAX_HEALTH

    def is_dead(self):
        """True iff a character's health is <= 0."""
        return self._health <= 0
