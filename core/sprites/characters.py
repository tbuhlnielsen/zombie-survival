
"""Zombie survival game

core.sprites.characters - Classes representing the main in-game characters.
"""

import random
import pygame as pg

from core.sprite import Character
from core.sprites.items import Gun, Pistol
from core.tools.collisions import axis_collide

from constants.settings import *


class Player(Character):
    """A survivor of the zombie invasion."""

    def __init__(self, game, x, y, img, max_speed=200, max_spin_rate=250):
        """A Player starts out with a Pistol."""
        super().__init__(game, x, y, img, max_speed, max_spin_rate)

        self.weapon = Pistol(self.game, owner=self)

        # appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

        # groups
        self.game.get_scene().all_sprites.add(self)

    def use_weapon(self):
        """Checks to see which kind of Weapon a Player has and then uses it."""
        if isinstance(self.weapon, Gun):
            position = (self.position
                        + self.weapon.barrel_offset.rotate(-self.rotation))

            direction = pg.math.Vector2(1, 0).rotate(-self.rotation)
            offset = random.uniform(-self.weapon.spread, self.weapon.spread)

            self.weapon.fire(position, direction.rotate(offset))

    def check_item_pickup(self):
        """Returns any Items a Player walks over."""
        # dokill == False because a Player might not intend to pick up an item
        # e.g. not picking up a health pack when health is already full
        return pg.sprite.spritecollide(self, self.game.get_scene().items, False)

    def add_health(self, amount):
        """Adds amount health to a Player."""
        self.health = min(self.max_health, self.health + amount)

    def rotate(self, keys, dt):
        """Rotate a Player in response to key presses."""
        # only rotate if a key is pressed
        self.rotate_speed = 0

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotate_speed = self.max_spin_rate

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotate_speed = -self.max_spin_rate

        self.rotation = (self.rotation + self.rotate_speed * dt) % 360
        self.rotate_image()

    def move(self, keys, dt):
        """Update a Player's position and velocity in response to key
        presses.
        """
        # only move if a key is pressed
        self.velocity = pg.math.Vector2(0, 0)

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.velocity = pg.math.Vector2(self.max_speed, 0).rotate(-self.rotation)

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # Go at half speed when moving backwards.
            self.velocity = pg.math.Vector2(-self.max_speed/2, 0).rotate(-self.rotation)

        self.position += self.velocity * dt

    def update(self):
        """Rotate, move, and check for collisions with obstacles."""
        dt = self.game.get_scene().dt

        keys = pg.key.get_pressed()

        self.rotate(keys, dt)
        self.move(keys, dt)

        if keys[pg.K_SPACE]:
            self.use_weapon()

        self.check_for_collide()


class Zombie(Character):
    """Chases a Player."""

    def __init__(self, game, x, y, img, max_speed=150, max_spin_rate=None):
        """Initialises a Zombie at tile location (x, y)."""

        super().__init__(game, x, y, img, max_speed, max_spin_rate)

        # mechanics
        self.speeds = [self.max_speed - 10 * i for i in range(5)]
        self.speed = random.choice(self.speeds)

        # AI
        self.avoid_radius = 50 # pixels, for avoiding other Zombies
        self.sight_radius = 400 # a Zombie can only "see" a Player in this radius
        self.target = self.game.get_scene().player

        # appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

        # groups
        self.game.get_scene().all_sprites.add(self)
        self.game.get_scene().zombies.add(self)

    def draw_health(self):
        """Adds a health bar above a Zombie."""
        if self.health > 60:
            color = pg.Color("green")

        elif self.health > 30:
            color = pg.Color("yellow")

        else:
            color = pg.Color("red")

        width = int(self.rect.width * self.health / self.max_health)
        height = 5
        self.health_rect = pg.Rect(0, 0, width, height)

        if self.health < self.max_health:
            pg.draw.rect(self.image, color, self.health_rect)

    def rotate_to_player(self):
        """Rotates a Zombie in the direction of the Player."""
        x_hat = pg.math.Vector2(1, 0)

        self.rotation = (self.target.position - self.position).angle_to(x_hat)
        self.rotate_image()

    def avoid_others(self):
        """Ensures a Zombie doesn't clump together with other zombies in a
        single 'pile'.
        """
        for z in self.game.get_scene().zombies:
            if z != self:
                d = self.position - z.position
                if 0 < d.length_squared() < self.avoid_radius ** 2:
                    self.acceleration += d.normalize()

        self.acceleration.scale_to_length(self.speed)

    def move(self, dt):
        """Uses equations of motion to update a Zombie's acceleration, velocity,
        and position.
        """
        self.acceleration = pg.math.Vector2(1, 0).rotate(-self.rotation)
        self.avoid_others()
        self.acceleration += -self.velocity # friction

        self.velocity += self.acceleration * dt

        self.position += (self.velocity * dt
                          + 0.5 * self.acceleration * (dt ** 2))

    def update(self):
        """Makes a Zombie chase a Player if the Player is in range or the
        Player has shot the Zombie.
        """
        dt = self.game.get_scene().dt

        target_distance2 = (self.target.position-self.position).length_squared()

        if target_distance2 < self.sight_radius ** 2 or self.is_injured():
            self.rotate_to_player()
            self.move(dt)
            self.check_for_collide()

            # play a sound effect once in a while
            if random.random() < 0.002:
                random.choice(self.game.zombie_groans).play()

        if self.health <= 0:
            # play sound effect
            self.kill()
