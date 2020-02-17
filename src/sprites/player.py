
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import settings
import sprites.behaviour
import sprites.template

# ==============================================================================

class Player(sprites.template.MovingEntity):
    """A survivor of the zombie invasion."""

    def __init__(self, x, y, img, speed=160, spin_rate=240):
        """Initialise a Player at tile location (x, y)."""
        super().__init__(x, y, img, speed, spin_rate)
        self.image = pg.transform.scale(self.original_image,
                                        settings.TILE_AREA)
        self.rect = self.image.get_rect()

    def rotate(self, dt):
        """Rotate a Player in response to keys presses."""
        self.rotate_speed = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rotate_speed = self.spin_rate

        if keys[pg.K_RIGHT]:
            self.rotate_speed = -self.spin_rate

        self.rotation = (self.rotation + self.rotate_speed * dt) % 360
        self.rotate_image()
        self.rect.center = self.position

    def move(self, dt):
        """Update a Player's position and velocity in response to key
        presses.
        """
        self.velocity = pg.math.Vector2(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.velocity = pg.math.Vector2(self.speed, 0).rotate(-self.rotation)

        if keys[pg.K_DOWN]: # half speed when moving backwards
            self.velocity = pg.math.Vector2(-self.speed / 2, 0).rotate(-self.rotation)

        self.position += self.velocity * dt

    def check_for_collide(self, walls):
        """Updates a Player's position if it collides with walls."""
        self.hit_rect.centerx = self.position.x
        sprites.behaviour.collision(self, walls, "x")

        self.hit_rect.centery = self.position.y
        sprites.behaviour.collision(self, walls, "y")

        self.rect.center = self.hit_rect.center

    def update(self, dt, walls):
        """Rotate, move, and check for collisions with walls."""
        self.rotate(dt)
        self.move(dt)
        self.check_for_collide(walls)
