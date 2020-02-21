
"""Zombie survival game

constants.paths - Constants defining local file locations.
"""

from os import path

# ==============================================================================

CONST_DIR = path.dirname(__file__)

# root
(ROOT_DIR, _) = path.split(CONST_DIR)

# assets
ASSETS_DIR = path.join(ROOT_DIR, "assets")
ANIMATION_DIR = path.join(ASSETS_DIR, "animations")
IMG_DIR = path.join(ASSETS_DIR, "images")
MAPS_DIR = path.join(ASSETS_DIR, "maps")
MUSIC_DIR = path.join(ASSETS_DIR, "music")
SOUND_DIR = path.join(ASSETS_DIR, "sounds")

# core
CORE_DIR = path.join(ROOT_DIR, "core")
