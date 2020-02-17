
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

class Mob(sprites.template.MovingEntity):
    """A zombie that chases a Player"""

    def __init__(self, x, y, img, speed=150, spin_rate=None):
        """Initialises a Mob at tile location (x, y)."""
        super().__init__(x, y, img, speed, spin_rate)
        self.image = pg.transform.scale(self.original_image,
                                        settings.TILE_AREA)
        self.rect = self.image.get_rect()

    def rotate_to(self, target):
        """Rotates a Mob in the direction of target."""
        x_hat = pg.math.Vector2(1, 0)

        self.rotation = (target.position-self.position).angle_to(x_hat)
        self.rotate_image()

    def move(self, dt):
        """Uses equations of motion to update a Mob's mechanical attributes."""
        self.acceleration = pg.math.Vector2(self.speed, 0).rotate(-self.rotation)
        self.acceleration += -self.velocity # friction

        self.velocity += self.acceleration*dt

        self.position += self.velocity*dt + 0.5*self.acceleration*(dt**2)

    def check_for_collide(self, walls):
        """Updates a Mob's position if it collides with walls."""
        self.hit_rect.centerx = self.position.x
        sprites.behaviour.collision(self, walls, "x")

        self.hit_rect.centery = self.position.y
        sprites.behaviour.collision(self, walls, "y")

        self.rect.center = self.hit_rect.center

    def update(self, dt, walls, target):
        """Makes a Mob chase a target."""
        self.rotate_to(target)
        self.move(dt)
        self.check_for_collide(walls)
