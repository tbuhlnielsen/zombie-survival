
"""Zombie survival game

core.ui.hud - Class for drawing HUD elements, functions for drawing objects to
              screen.
"""

import pygame as pg

from constants.settings import Tile, Window


class HUD:
    """A heads-up display."""

    def __init__(self, game):
        """Set up all the HUD elements."""
        self.game = game
        self.player_health_bar = PlayerHealthBar(10, 10, 100, 20)

    def draw(self):
        """Draws all the HUD elements to the game screen."""
        self.player_health_bar.draw(self.game.screen,
                                    self.game.active_scene.player.health)


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
            color = pg.Color("green")

        elif p > 30:
            color = pg.Color("yellow")

        else:
            color = pg.Color("red")

        pg.draw.rect(surf, color, fill_rect)
        pg.draw.rect(surf, pg.Color("white"), outline_rect, 2) # 2px border


def draw_text(surf, text, size=16, x=Window["width"]//2, y=Window["height"]//2,
              color=pg.Color("white")):
    """Draws text on surf centred at pixel location (x, y). Uses the
    system's default font.
    """
    font = pg.font.Font(pg.font.get_default_font(), size)
    text_surf = font.render(text, True, color) # True for anti-alias

    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)

    surf.blit(text_surf, text_rect)


def draw_grid(surf):
    """Draws the tile grid on surf."""
    # vertical lines
    for x in range(0, Tile["num_x"]):
        pg.draw.line(surf, pg.Color("grey50"),
                     (x * Tile["size"], 0),
                     (x * Tile["size"], Window["height"]))

    # horizontal lines
    for y in range(0, Tile["num_y"]):
        pg.draw.line(surf, pg.Color("grey50"),
                     (0, y * Tile["size"]),
                     (Window["height"], y * Tile["size"]))
