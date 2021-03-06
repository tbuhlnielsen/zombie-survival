
"""Zombie survival game

core.sprites.items - Classes for weapons and items that a Player can pick up.
"""

import pygame as pg
import pytweening as tween

from core.ui.animations import GunFire

from constants.settings import *


# shorten name
vec = pg.math.Vector2

# stats for various weapons
WEAPONS = {
    "pistol": {
        "damage": 10,
        "accuracy": 80,
        "barrel_offset": vec(25, 10),
        "bullet_count": 1,
        "bullet_speed": 400, # should scale
        "range_": 60,
        "recoil": 5,
        "reload_time": 20 # should scale
    }
}


class Weapon:
    """Base class for an in-game weapon.

    For simplicity, a Weapon's stats should be in the range [0, 100].
    These are then scaled with various 'calc' functions (see below) so that
    they look reasonable in-game.
    """

    def __init__(self, game, damage, owner=None):
        """Sets up some attributes common to all Weapons."""
        self.game = game

        self.damage = damage
        self.owner = owner

        # for controlling how often a Player can use the Weapon.
        self.last_used = 0


class Gun(Weapon):
    """Base class for a Bullet-firing weapon."""

    def __init__(self, game, damage, accuracy, barrel_offset, range_, recoil,
                 reload_time, bullet_count, bullet_speed, owner=None):
        """ """
        super().__init__(game, damage, owner)

        self.spread = calc_spread(accuracy)

        # used to spawn Bullets from an appropriate location on the sprite of
        # the Gun's owner
        self.barrel_offset = barrel_offset

        self.bullet_count = bullet_count
        self.bullet_speed = bullet_speed

        self.range = range_
        self.recoil = recoil
        self.fire_rate = calc_fire_rate(reload_time)


    def fire(self, position, directions):
        """Fires a Bullet from position towards direction."""
        now = pg.time.get_ticks()

        if now - self.last_used > self.fire_rate:
            self.last_used = now

            for d in directions:
                b = Bullet(self.game, position, d, self.bullet_speed, self.range)

            self.anim = GunFire(self.game, position)

            snd = self.game.gun_sounds["pistol_sound"]
            if snd.get_num_channels() > 2:
                snd.stop()
            snd.play()

            # Add recoil.
            # if self.owner:
                # Move slightly.


def calc_fire_rate(reload_time):
    """Calculates the fire rate of a Gun using a linear relationship with
    reload_time.
    """
    # "y - y0 = m * (x - x0)"
    (x0, y0) = (0, 100) # reload_time == 0 -> fire_rate == 100 (ms)
    (x1, y1) = (100, 1000) # reload_time == 100 -> fire_rate == 1000 (ms)

    m = (y1 - y0) / (x1 - x0)

    return m * (reload_time - x0) + y0


def calc_spread(accuracy):
    """Calculates the spread of a Gun using a linear relationship with
    accuracy."""
    # "y - y0 = m * (x - x0)"
    (x0, y0) = (0, 20) # accuracy == 0 -> spread == 25 (pixels)
    (x1, y1) = (100, 0) # accuracy == 100 -> spread == 0

    m = (y1 - y0) / (x1 - x0)

    return m * (accuracy - x0) + y0


class Bullet(pg.sprite.Sprite):
    """Fired by a Gun."""

    def __init__(self, game, position, direction, speed, gun_range):
        """A Bullet is passed the range of the Gun that fires it in order to
        calculate how far it should travel before disappearing.
        """
        self._layer = WEAPON_LAYER
        super().__init__()

        self.game = game
        self.game.get_scene().all_sprites.add(self)
        self.game.get_scene().ammo.add(self)

        # Mechanics
        self.position = vec(position) # can't use position directly as this
                                      # would modify the position of whoever
                                      # fired the bullet

        self.speed = speed
        self.velocity = direction * self.speed

        # Appearance
        self.image = self.game.bullet_image

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.hit_rect = self.rect

        self.spawn_time = pg.time.get_ticks()
        self.lifetime = calc_lifetime(gun_range)

    def update(self):
        """Updates the position of a Bullet and checks for collisions with
        obstacles. Makes the Bullet disappear after it has been on screen
        for the duration of its lifetime.
        """
        dt = self.game.get_scene().dt

        self.position += self.velocity * dt
        self.rect.center = self.position

        if pg.sprite.spritecollideany(self, self.game.get_scene().obstacles):
            self.kill()

        now = pg.time.get_ticks()
        if now - self.spawn_time > self.lifetime:
            self.kill()


def calc_lifetime(range_):
    """Calculates the lifetime of a Bullet using a linear relationship with
    range_."""
    # "y - y0 = m * (x - x0)"
    (x0, y0) = (0, 0) # range_ == 0 -> lifetime == 100 (ms)
    (x1, y1) = (100, 2000) # range_ == 100 -> lifetime == 2000 (ms)

    m = (y1 - y0) / (x1 - x0)

    return m * (range_ - x0) + y0


class Item(pg.sprite.Sprite):
    """Base class for an item that a Player can pick up."""

    def __init__(self, game, position, kind):
        """Spawn an Item at position."""
        self._layer = ITEM_LAYER
        super().__init__()

        self.game = game

        self.position = position

        # groups
        self.game.get_scene().all_sprites.add(self)
        self.game.get_scene().items.add(self)

        # appearance
        self.kind = kind
        self.image = self.game.item_images[kind]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.hit_rect = self.rect

        self.tween = tween.easeInOutSine # Bobbing animation
        self.bob_range = 16
        self.bob_speed = 0.4
        self.step = 0 # Between start and end of bobbing
        self.y_direction = 1 # Down screen; -1 is up screen

    def update(self):
        """Bob an Item up and down."""
        # take off 0.5 to start in center of range
        offset = self.bob_range * (self.tween(self.step / self.bob_range) - 0.5)

        self.rect.centery = self.position.y + offset * self.y_direction

        self.step += self.bob_speed
        if self.step > self.bob_range:
            self.step = 0
            self.y_direction *= -1
