
"""Zombie survival game

core.tools.collisions - Functions for detecting collisions between game objects.

TO DO: explain axis_collide().
"""

import pygame as pg

from core.sprites.items import Gun

from constants.settings import *

# shorten name
vec = pg.math.Vector2


def collide_hit_rect(A, B):
    """Detect a collision between two sprites A and B using the hit_rect
    of A.
    """
    return A.hit_rect.colliderect(B.rect)


def axis_collide(sprite, group, axis):
    """Check for collisions between sprite and group using collide_hit_rect().
    """
    # False => don't kill the objects in group that intersect sprite
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

    if hits:
        h = hits[0]
        if axis == "x":
            if h.rect.centerx > sprite.hit_rect.centerx:
                sprite.position.x = h.rect.left - sprite.hit_rect.width/2
                # position tracks the center of sprite

            if h.rect.centerx < sprite.hit_rect.centerx:
                sprite.position.x = h.rect.right + sprite.hit_rect.width/2

            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x

        if axis == "y":
            if h.rect.centery > sprite.hit_rect.centery:
                sprite.position.y = h.rect.top - sprite.hit_rect.height/2

            if h.rect.centery < sprite.hit_rect.centery:
                sprite.position.y = h.rect.bottom + sprite.hit_rect.height/2

            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y


def obstacle_collide(character, obstacles):
    """Updates a character's position if it collides with an obstacle."""
    character.hit_rect.centerx = character.position.x
    axis_collide(character, obstacles, "x")

    character.hit_rect.centery = character.position.y
    axis_collide(character, obstacles, "y")

    character.rect.center = character.hit_rect.center


def item_pickup(player, items):
    """Checks if a player picked up an item and, if so, applies its effect."""
    # False => don't yet kill() item - player might not have meant to pick it up
    hits = pg.sprite.spritecollide(player, items, False)

    for item in hits:
        if item.kind == HEALTH_ITEM_TILE and player.is_injured():
            player.increase_health(HEALTH_PACK_VALUE)
            item.kill()


def player_hit(player, zombies):
    """Applies damage to player if hit by zombies."""
    # False => don't kill zombies
    z_hits = pg.sprite.spritecollide(player, zombies, False, collide_hit_rect)

    for z in z_hits:
        player.increase_health(-10)
        z.velocity = vec(0, 0) # zombie stops if it hits player

    # knock player back a little
    if z_hits:
        player.position += pg.math.Vector2(20, 0).rotate(-z_hits[0].rotation)


def zombies_hit(zombies, ammo, damage):
    """Applies damage to zombies hit by ammo."""
    # False, True => don't immediately kill() zombies, but do kill() ammo
    z_hits = pg.sprite.groupcollide(zombies, ammo, False, True)

    for z in z_hits:
        # take off health for each bullet that hits the zombie
        z.increase_health(-damage * len(z_hits[z]))
        z.velocity = vec(0, 0) # zombie briefly stops when hit
