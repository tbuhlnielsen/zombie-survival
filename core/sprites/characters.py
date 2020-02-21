
"""Zombie survival game

core.sprites.characters - Classes representing the main in-game characters.
"""

import random

import pygame as pg

from core.tools.collisions import axis_collide
from core.sprites.items import Gun, Pistol
from constants.settings import Layer, Tile


class Character(pg.sprite.Sprite):
    """Base class for a character that can move, rotate, and collide with
    other game objects.
    """

    def __init__(self, game, x, y, img, max_speed, max_spin_rate):
        """Set up the mechanics and appearance of a Character."""
        self._layer = Layer["character"]
        super().__init__()

        self.game = game

        # Mechanics
        self.position = pg.math.Vector2(x, y)

        self.max_speed = max_speed # pixels per second
        self.velocity = pg.math.Vector2(0, 0) # set components to +- max_speed

        self.acceleration = pg.math.Vector2(0, 0)

        self.max_spin_rate = max_spin_rate # degrees per second
        self.rotate_speed = 0 # set to +- max_spin_rate
        self.rotation = 0 # degrees

        # Appearance
        self.original_image = img # for applying transformations to
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Collision rect
        s = int(Tile["size"] * 0.75)
        self.hit_rect = pg.Rect(0, 0, s, s)
        self.hit_rect.center = (x, y)

    def rotate_image(self):
        """Updates self.image by rotating self.original_image."""
        self.image = pg.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def check_for_collide(self):
        """Updates a Character's position if it collides with an obstacle."""
        self.hit_rect.centerx = self.position.x
        axis_collide(self, self.game.active_scene.obstacles, "x")

        self.hit_rect.centery = self.position.y
        axis_collide(self, self.game.active_scene.obstacles, "y")

        self.rect.center = self.hit_rect.center


class Player(Character):
    """A survivor of the zombie invasion."""

    def __init__(self, game, x, y, img, max_speed=200, max_spin_rate=250):
        """A Player starts out with a Pistol."""
        super().__init__(game, x, y, img, max_speed, max_spin_rate)

        self.max_health = 100
        self.health = self.max_health

        self.weapon = Pistol(self.game, owner=self)

        # Groups
        self.game.active_scene.all_sprites.add(self)

        # Appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

    def use_weapon(self):
        """Checks to see which kind of Weapon a Player has and then uses it."""
        if isinstance(self.weapon, Gun):
            position = (self.position
                        + self.weapon.barrel_offset.rotate(-self.rotation))
            direction = pg.math.Vector2(1, 0).rotate(-self.rotation)
            offset = random.uniform(-self.weapon.spread, self.weapon.spread)

            self.weapon.fire(position, direction.rotate(offset))

    def check_item_pickup(self):
        """Returns any Items picked up by a Player."""
        return pg.sprite.spritecollide(self, self.game.active_scene.items, False)

    def add_health(self, amount):
        """Adds amount health to a Player."""
        self.health = min(self.max_health, self.health + amount)

    def rotate(self, keys):
        """Rotate a Player in response to key presses."""
        self.rotate_speed = 0
        dt = self.game.frame_duration

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotate_speed = self.max_spin_rate

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotate_speed = -self.max_spin_rate

        self.rotation = (self.rotation + self.rotate_speed * dt) % 360
        self.rotate_image()

    def move(self, keys):
        """Update a Player's position and velocity in response to key
        presses.
        """
        self.velocity = pg.math.Vector2(0, 0)
        dt = self.game.frame_duration

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.velocity = pg.math.Vector2(self.max_speed, 0).rotate(-self.rotation)

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # Go at half speed when moving backwards.
            self.velocity = pg.math.Vector2(-self.max_speed/2, 0).rotate(-self.rotation)

        self.position += self.velocity * dt

    def update(self):
        """Rotate, move, and check for collisions with obstacles."""
        keys = pg.key.get_pressed()

        self.rotate(keys)
        self.move(keys)

        if keys[pg.K_SPACE]:
            self.use_weapon()

        self.check_for_collide()


class Zombie(Character):
    """Chases a Player."""

    def __init__(self, game, x, y, img, max_speed=150, max_spin_rate=None):
        """Initialises a Zombie at tile location (x, y)."""

        super().__init__(game, x, y, img, max_speed, max_spin_rate)

        # Mechanics
        self.speeds = [self.max_speed - 10 * i for i in range(5)]
        self.speed = random.choice(self.speeds)

        # Health
        self.max_health = 100
        self.health = self.max_health

        # AI
        self.avoid_radius = 50 # pixels
        self.sight_radius = 400 # A Zombie can only "see" a Player in this radius
        self.target = self.game.active_scene.player

        # Groups
        self.game.active_scene.all_sprites.add(self)
        self.game.active_scene.zombies.add(self)

        # Appearance
        # self.image = pg.transform.scale(self.original_image, Tile["area"])
        # self.rect = self.image.get_rect()
        # position rect

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
        for z in self.game.active_scene.zombies:
            if z != self:
                d = self.position - z.position
                if 0 < d.length() < self.avoid_radius:
                    self.acceleration += d.normalize()

        self.acceleration.scale_to_length(self.speed)

    def move(self):
        """Uses equations of motion to update a Zombie's acceleration, velocity,
        and position.
        """
        dt = self.game.frame_duration

        self.acceleration = pg.math.Vector2(1, 0).rotate(-self.rotation)
        self.avoid_others()
        self.acceleration += -self.velocity # friction

        self.velocity += self.acceleration * dt

        self.position += (self.velocity * dt
                          + 0.5 * self.acceleration * (dt ** 2))

    def is_injured(self):
        """True iff a Zombie's health has decreased."""
        return self.health < self.max_health

    def update(self):
        """Makes a Zombie chase a Player if the Player is in range or the
        Player has shot the Zombie.
        """
        target_distance2 = (self.target.position-self.position).length_squared()

        if target_distance2 < self.sight_radius ** 2 or self.is_injured():
            self.rotate_to_player()
            self.move()
            self.check_for_collide()

            if random.random() < 0.002:
                random.choice(self.game.zombie_sound_effects).play()

        if self.health <= 0:
            self.kill()
            # self.game.zombie_death_effect.play()
