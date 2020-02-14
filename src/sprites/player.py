
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import settings
import sprites.behaviour

# ==============================================================================

class Player(pg.sprite.Sprite):
    """A survivor of the zombie invasion."""

    def __init__(self, x, y, speed=160, turn_rate=240):
        """Initialise a Player at tile location (x, y)."""
        super().__init__()
        self.original_image = fx.load_image("survivor_gun.png") # to be rotated
        self.original_image = pg.transform.scale(self.original_image,
                                                 settings.TILE_AREA)
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 22, 22)
        self.hit_rect.center = self.rect.center

        self.position = pg.math.Vector2(x, y) * settings.TILE_SIZE

        self.speed = speed
        self.velocity = pg.math.Vector2(0, 0) # set components to +- speed

        self.rotation = 0
        self.turn_rate = turn_rate # degrees per second
        self.rotate_speed = 0 # set to +- turn speed

    def rotate(self):
        """Rotate the Player image."""
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def move(self):
        """Update the Player's velocity when keys are pressed."""
        self.velocity[:] = 0, 0
        self.rotate_speed = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.rotate_speed = self.turn_rate

        if keys[pg.K_RIGHT]:
            self.rotate_speed = -self.turn_rate

        if keys[pg.K_UP]:
            self.velocity = pg.math.Vector2(self.speed, 0).rotate(-self.rotation)

        if keys[pg.K_DOWN]: # half speed when moving backwards
            self.velocity = pg.math.Vector2(-self.speed / 2, 0).rotate(-self.rotation)

    def update(self, dt, walls):
        """Rotate, move, and check for collisions with walls."""
        self.rotate()
        self.rotation = (self.rotation + self.rotate_speed * dt) % 360

        self.move()
        self.position += self.velocity * dt

        self.hit_rect.centerx = self.position.x
        sprites.behaviour.collision(self, walls, "x")

        self.hit_rect.centery = self.position.y
        sprites.behaviour.collision(self, walls, "y")

        self.rect.center = self.hit_rect.center
