
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import os
import pygame as pg

from typing import List, Tuple

import settings

# ==============================================================================

(ROOT_DIR, _) = os.path.split(os.path.dirname(__file__))
IMG_DIR = os.path.join(ROOT_DIR, "assets", "images")
AUDIO_DIR = os.path.join(ROOT_DIR, "assets", "sounds")

# ---------------------------------------

def load_image(file_name: str) -> pg.Surface:
    """Loads an image from IMG_DIR."""
    full_name = os.path.join(IMG_DIR, file_name)

    img = pg.image.load(full_name)
    img = img.convert_alpha()

    return img

# ---------------------------------------

def draw_text(game_screen: pg.Surface, text: str, size: int=16,
              x: int=settings.WINDOW_WIDTH//2, y: int=settings.WINDOW_HEIGHT//2,
              color: Tuple[int]=settings.RGB_WHITE) -> None:
    """Draws text on game_screen centred at pixel location (x, y). Uses the
    system's default font.
    """
    font = pg.font.Font(pg.font.get_default_font(), size)
    surf = font.render(text, True, color) # True for anti-alias
    
    rect = surf.get_rect()
    rect.center = (x, y)

    game_screen.blit(surf, rect)

# ---------------------------------------

def draw_grid(game_screen: pg.Surface) -> None:
    """Draws the tile grid."""
    # vertical lines
    for x in range(0, settings.NUM_TILES_X):
        pg.draw.line(game_screen, settings.RGB_GREY,
                     (x * settings.TILE_SIZE, 0),
                     (x * settings.TILE_SIZE, settings.WINDOW_HEIGHT))

    # horizontal lines
    for y in range(0, settings.NUM_TILES_Y):
        pg.draw.line(game_screen, settings.RGB_GREY,
                     (0, y * settings.TILE_SIZE),
                     (settings.WINDOW_HEIGHT, y * settings.TILE_SIZE))
