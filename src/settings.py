
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

# tiles
TILE_SIZE = 32 # pixels
TILE_AREA = (TILE_SIZE, TILE_SIZE)
NUM_TILES_X = 24
NUM_TILES_Y = 20

PLAYER_SYMBOL = "P"
WALL_SYMBOL = "1"
MOB_SYMBOL = "M"

# window
FPS = 60
WINDOW_WIDTH = NUM_TILES_X * TILE_SIZE
WINDOW_HEIGHT = NUM_TILES_Y * TILE_SIZE
WINDOW_AREA = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Black and white
RGB_BLACK = (0, 0, 0)
RGB_GREY = (127, 127, 127)
RGB_WHITE = (255, 255, 255)

# Primary
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)

# Secondary
RGB_CYAN = (0, 255, 255)

# Custom
BG_COLOR = (105, 55, 5)
