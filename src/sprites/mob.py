
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

class Mob(pg.sprite.Sprite):

    def __init__(self, x, y, speed=150):
        """Initialise a Mob at tile location (x, y)."""
        super().__init__()

        self.original_image = fx.load_image("zombie_hold.png")
        self.image = pg.transform.scale(self.original_image, settings.TILE_AREA)

        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 22, 22)
        self.hit_rect.center = self.rect.center

        self.position = pg.math.Vector2(x, y) * settings.TILE_SIZE
        self.rect.center = self.position

        self.speed = speed
        self.velocity = pg.math.Vector2(0, 0) # set components to +- speed

        self.acceleration = pg.math.Vector2(0, 0)

        self.rotation = 0 # degrees

    def update(self, dt, walls, target):
        """Make a Mob chase a target."""
        x_unit_vec = pg.math.Vector2(1, 0)
        self.rotation = (target.position - self.position).angle_to(x_unit_vec)
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()

        self.acceleration = pg.math.Vector2(self.speed, 0).rotate(-self.rotation)
        self.acceleration += -self.velocity # friction
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt + 0.5 * self.acceleration * (dt ** 2)

        self.hit_rect.centerx = self.position.x
        sprites.behaviour.collision(self, walls, "x")

        self.hit_rect.centery = self.position.y
        sprites.behaviour.collision(self, walls, "y")

        self.rect.center = self.hit_rect.center
