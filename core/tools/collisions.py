
"""Zombie survival game

core.tools.collisions - Functions for detecting collisions between game objects.

TO DO: explain axis_collide().
"""

import pygame as pg


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
