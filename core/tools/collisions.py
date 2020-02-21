
"""Zombie survival game

core.tools.collisions - Functions for detecting collisions between game objects.
"""

import pygame as pg


def collide_hit_rect(sprite_A, sprite_B):
    """Detect a collision between sprite_A and sprite_B using their
    hit_rect attributes.
    """
    return sprite_A.hit_rect.colliderect(sprite_B.rect)


def axis_collide(sprite, group, axis):
    """Check for collisions between sprite and group.

    TO DO: explain axis.
    """
    # False means don't delete walls
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

    if hits:
        if axis == "x":
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.position.x = (hits[0].rect.left
                                     - sprite.hit_rect.width/2)

            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.position.x = (hits[0].rect.right
                                     + sprite.hit_rect.width/2)

            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x

        if axis == "y":
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.position.y = (hits[0].rect.top
                                     - sprite.hit_rect.height/2)

            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.position.y = (hits[0].rect.bottom
                                     + sprite.hit_rect.height/2)

            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y