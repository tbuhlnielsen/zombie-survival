
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import settings

# ==============================================================================

class Entity:
    """A game object with a position."""

    def __init__(self, x, y, img):
        """Set an Entity up at tile location (x, y)."""
        self.position = pg.math.Vector2(x, y) * settings.TILE_SIZE

        self.original_image = img
        self.image = img

class MovingEntity(Entity):
    """A game object which can move, collide with other game objects,
    and rotate.
    """

    def __init__(self, x, y, img, speed, spin_rate):
        super().__init__(x, y, img)

        self.speed = speed # pixels per second
        self.velocity = pg.math.Vector2(0, 0) # set components to +- speed

        self.acceleration = pg.math.Vector2(0, 0)

        self.spin_rate = spin_rate # degrees per second
        self.rotation = 0 # degrees
        self.rotate_speed = 0 # set to +- spin_rate

    def move(self):
        pass

    def rotate(self):
        pass

    def update(self):
        pass
