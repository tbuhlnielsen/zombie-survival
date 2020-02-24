
"""Zombie survival game

constants.paths - Constants defining local file locations. Used in resource
                  loading functions.
"""

from os import path


CONST_DIR = path.dirname(__file__)

(ROOT_DIR, _) = path.split(CONST_DIR)

ASSETS_DIR = path.join(ROOT_DIR, "assets")

IMG_DIR = path.join(ASSETS_DIR, "images")

MAPS_DIR = path.join(ASSETS_DIR, "maps")

SOUND_DIR = path.join(ASSETS_DIR, "sounds")

FONT_DIR = path.join(ASSETS_DIR, "fonts")
