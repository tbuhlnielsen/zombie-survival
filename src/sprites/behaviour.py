
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

def collide_hit_rect(sprite_A, sprite_B):
    return sprite_A.hit_rect.colliderect(sprite_B.rect)

def collision(sprite, group, axis):
    """Check for collisions between sprite and group."""
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    # False means don't delete walls

    if hits:
        if axis == "x":
            if sprite.velocity.x > 0:
                sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.velocity.x < 0:
                sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x

        if axis == "y":
            if sprite.velocity.y > 0:
                sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.velocity.y < 0:
                sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2

            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y
