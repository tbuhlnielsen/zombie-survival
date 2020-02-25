
"""Zombie survival game

core.ui.hud - Class for drawing HUD elements, functions for drawing objects to
              screen.
"""

import pygame as pg

from core.tools.resources import load_font

from constants.settings import *


class HUD:
    """A heads-up display."""

    def __init__(self, game):
        """Set up all the HUD elements."""
        self.game = game
        self.player_health_bar = PlayerHealthBar(x=10, y=10, w=100, h=20)

    def draw(self):
        """Draws all the HUD elements to the game screen."""
        self.player_health_bar.draw(self.game.screen,
                                    self.game.get_scene().player.get_health())


class PlayerHealthBar:
    """A bar showing a Player's remaining health."""

    def __init__(self, x, y, w, h):
        """Sets up the location and size of a PlayerHealthBar."""
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def draw(self, surf, p):
        """Draws a PlayerHealthBar (filled to p% of self.width) on surf."""
        fill = (p / 100) * self.width

        outline_rect = pg.Rect(self.x, self.y, self.width, self.height)
        fill_rect = pg.Rect(self.x, self.y, fill, self.height)

        if p > 60:
            color = GREEN

        elif p > 30:
            color = YELLOW

        else:
            color = RED

        pg.draw.rect(surf, color, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2) # 2px border


def draw_text(surf, text, size=16, color=WHITE, x=WIDTH//2, y=HEIGHT//2,
              align="center", font_name=None):
    """Draws text on surf at pixel (x, y)."""
    # use default font if necessary
    font_ = "kenvector-future.ttf" if not font_name else font_name
    font = load_font(font_, size)

    text_surf = font.render(text, True, color) # True for anti-alias
    text_rect = text_surf.get_rect()

    # choose alignment
    if align == "nw":
        text_rect.topleft = (x, y)

    if align == "ne":
        text_rect.topright = (x, y)

    if align == "sw":
        text_rect.bottomleft = (x, y)

    if align == "se":
        text_rect.bottomright = (x, y)

    if align == "n":
        text_rect.midtop = (x, y)

    if align == "s":
        text_rect.midbottom = (x, y)

    if align == "e":
        text_rect.midright = (x, y)

    if align == "w":
        text_rect.midleft = (x, y)

    if align == "center":
        text_rect.center = (x, y)

    text_rect.center = (x, y)
    surf.blit(text_surf, text_rect)


def draw_grid(surf, color=GREY):
    """Draws the tile grid on surf."""
    # vertical lines
    for x in range(NUM_X_TILES):
        pg.draw.line(surf, color,
                     (x * TILE_SIZE, 0),
                     (x * TILE_SIZE, HEIGHT))

    # horizontal lines
    for y in range(NUM_Y_TILES):
        pg.draw.line(surf, color,
                     (0, y * TILE_SIZE),
                     (HEIGHT, y * TILE_SIZE))
