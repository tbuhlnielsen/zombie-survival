
"""Zombie survival game

constants.settings - Constants defining some global game settings.
"""

# drawing layers
OBSTACLE_LAYER = 1
ITEM_LAYER = 1

CHARACTER_LAYER = 2

WEAPON_LAYER = 3

FX_LAYER = 4

# grid
TILE_SIZE = 32 # pixels
TILE_AREA = (TILE_SIZE, TILE_SIZE)
NUM_X_TILES = 32
NUM_Y_TILES = 24

# display
FPS = 60
WINDOW_AREA = (WIDTH, HEIGHT) = (NUM_X_TILES * TILE_SIZE,
                                 NUM_Y_TILES * TILE_SIZE)
