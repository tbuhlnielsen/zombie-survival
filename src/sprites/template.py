
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import settings

# ==============================================================================

class Entity(pg.sprite.Sprite):
    """A game object with a position."""

    def __init__(self, x, y, img):
        """Set an Entity up at tile location (x, y).

        TO DO: why use original_image attribute?
        """
        super().__init__()
        self.position = pg.math.Vector2(x, y) * settings.TILE_SIZE

        self.original_image = img
        self.image = self.original_image

        self.rect = self.image.get_rect()

# ---------------------------------------

class MovingEntity(Entity):
    """A game object which can move, collide with other game objects,
    and rotate.
    """

    def __init__(self, x, y, img, speed, spin_rate):
        super().__init__(x, y, img)

        self.hit_rect = pg.Rect(0, 0, 22, 22) # change
        self.hit_rect.center = self.rect.center

        self.speed = speed # pixels per second
        self.velocity = pg.math.Vector2(0, 0) # set components to +- speed

        self.acceleration = pg.math.Vector2(0, 0)

        self.spin_rate = spin_rate # degrees per second
        self.rotation = 0 # degrees
        self.rotate_speed = 0 # set to +- spin_rate

    def rotate_image(self):
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()
