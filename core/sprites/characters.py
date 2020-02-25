
"""Zombie survival game

core.sprites.characters - Classes representing the main in-game characters.
"""

import random
import pygame as pg

from core.sprite import Character
from core.sprites.items import Gun, WEAPONS

from core.tools.collisions import obstacle_collide

from constants.settings import *


# shorten name
vec = pg.math.Vector2


class Player(Character):
    """A survivor of the zombie invasion."""

    def __init__(self, game, x, y, image, max_speed=200):
        """Starts a player out with a pistol."""
        super().__init__(game, x, y, image, max_speed)

        self.weapon = Gun(self.game, **WEAPONS["pistol"])

        # appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

        # groups
        self.game.get_scene().all_sprites.add(self)

    def use_weapon(self):
        """Checks to see which kind of weapon a player has and then uses it."""
        position = (self.position
                    + self.weapon.barrel_offset.rotate(-self.rotation))

        d = vec(1, 0).rotate(-self.rotation)
        offsets = [random.uniform(-self.weapon.spread, self.weapon.spread) \
                    for _ in range(self.weapon.bullet_count)]
        directions = [d.rotate(ofs) for ofs in offsets]

        self.weapon.fire(position, directions)

    def rotate(self, keys, dt):
        """Rotate a player in response to key presses."""
        # only rotate if a key is pressed
        self.rotate_speed = 0

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotate_speed = MAX_SPIN_RATE

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotate_speed = -MAX_SPIN_RATE

        self.rotation = (self.rotation + self.rotate_speed * dt) % 360
        self.rotate_image()

    def move(self, keys, dt):
        """Update a player's position and velocity in response to key
        presses.
        """
        # only move if a key is pressed
        self.velocity = vec(0, 0)

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.velocity = vec(self.max_speed, 0).rotate(-self.rotation)

        # go at half speed when moving backwards
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.velocity = vec(-self.max_speed/2, 0).rotate(-self.rotation)

        self.position += self.velocity * dt

    def update(self):
        """Rotate, move, and check for collisions with obstacles."""
        dt = self.game.get_scene().dt

        keys = pg.key.get_pressed()

        self.rotate(keys, dt)
        self.move(keys, dt)

        if keys[pg.K_SPACE]:
            self.use_weapon()

        obstacle_collide(self, self.game.get_scene().obstacles)


class Zombie(Character):
    """Chases a Player."""

    def __init__(self, game, x, y, image, max_speed=175):
        """Initialises a Zombie at tile location (x, y)."""
        super().__init__(game, x, y, image, max_speed)

        # mechanics
        speeds = [self.max_speed - 10*i for i in range(5)]
        self.speed = random.choice(speeds)

        # AI
        self.avoid_radius = 50 # pixels, for avoiding other Zombies
        self.sight_radius = 400 # a zombie can only "see" a player in this radius
        self.target = self.game.get_scene().player

        # appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

        # groups
        self.game.get_scene().all_sprites.add(self)
        self.game.get_scene().zombies.add(self)

    def draw_health(self):
        """Adds a health bar above a zombie."""
        if self._health > 60:
            color = GREEN

        elif self._health > 30:
            color = YELLOW

        else:
            color = RED

        width = int(self.rect.width * self._health / MAX_HEALTH)
        height = 5
        self.health_rect = pg.Rect(0, 0, width, height) # does this need to be self.health_rect?

        if self.is_injured():
            pg.draw.rect(self.image, color, self.health_rect)

    def rotate_to_player(self):
        """Rotates a zombie in the direction of the player."""
        x_hat = vec(1, 0)
        self.rotation = (self.target.position - self.position).angle_to(x_hat)
        self.rotate_image()

    def avoid_others(self):
        """Ensures a zombie doesn't clump together with other zombies in a
        single 'pile'.
        """
        for z in self.game.get_scene().zombies:
            if z != self:
                d = self.position - z.position
                if 0 < d.length_squared() < self.avoid_radius ** 2:
                    self.acceleration += d.normalize()

        self.acceleration.scale_to_length(self.speed)

    def move(self, dt):
        """Uses equations of motion to update a zombie's acceleration, velocity,
        and position.
        """
        self.acceleration = vec(1, 0).rotate(-self.rotation)
        self.avoid_others()
        self.acceleration += -self.velocity # friction

        self.velocity += self.acceleration * dt

        self.position += (self.velocity * dt
                          + 0.5 * self.acceleration * (dt ** 2))

    def update(self):
        """Makes a zombie chase a player if the player is in range or the
        player has shot the Zombie.
        """
        dt = self.game.get_scene().dt

        target_distance2 = (self.target.position-self.position).length_squared()
        if target_distance2 < self.sight_radius ** 2 or self.is_injured():
            self.rotate_to_player()
            self.move(dt)
            obstacle_collide(self, self.game.get_scene().obstacles)

            # play a sound effect once in a while
            if random.random() < 0.002:
                random.choice(self.game.zombie_groans).play()

    def run_death_sequence(self):
        """Called when a zombie dies - play a sound effect and leave a splat."""
        self.kill()

        # play sound effect

        s = random.choice(self.game.splat_images)
        splat = pg.transform.scale(s, (TILE_SIZE * 2, TILE_SIZE * 2))
        offset = vec(TILE_SIZE, TILE_SIZE)
        self.game.get_scene().map_image.blit(splat, self.position - offset)
