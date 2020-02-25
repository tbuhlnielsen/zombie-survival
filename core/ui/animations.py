
"""Zombie survival game

core.sprites.animations - Classes representing in-game animations.
"""

import pygame as pg

import random

from constants.settings import FX_LAYER


class Animation(pg.sprite.Sprite):
    """Base class for all animations."""

    def __init__(self, game, duration):
        """Set up the layer and duration of an Animation."""
        self._layer = FX_LAYER
        super().__init__()

        self.game = game
        self.game.get_scene().all_sprites.add(self)

        self.spawn_time = pg.time.get_ticks()
        self.duration = duration # ms

    def update(self):
        """Stop an Animation when it has existed for its duration."""
        now = pg.time.get_ticks()
        if now - self.spawn_time > self.duration:
            self.kill()


class GunFire(Animation):
    """The animation that plays when a Gun is fired."""

    def __init__(self, game, position, duration=40):
        """Sets up the location and appearance of a GunFire animation."""
        super().__init__(game, duration)

        self.position = position

        # appearance
        size = random.randint(20, 40) # pixels
        frame = random.choice(self.game.smoke_animation)
        self.image = pg.transform.scale(frame, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.hit_rect = self.rect # for debugging
