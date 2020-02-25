
"""Zombie survival game

constants.settings - Constants defining some global game settings.
"""

# drawing layers
OBSTACLE_LAYER = ITEM_LAYER = 1
CHARACTER_LAYER = 2
WEAPON_LAYER = 3
FX_LAYER = 4

PLAYER_TILE = "player"
ZOMBIE_TILE = "zombie"
OBSTACLE_TILE = "wall" # change in .tmx files
HEALTH_ITEM_TILE = "health"

# items
HEALTH_PACK_VALUE = 50

# character attributes
MAX_HEALTH = 100
MAX_SPIN_RATE = 250

# grid
TILE_SIZE = 32 # pixels
TILE_AREA = (TILE_SIZE, TILE_SIZE)
NUM_X_TILES = 32
NUM_Y_TILES = 24

# display
FPS = 60
TITLE = "Zombie Survival"
WINDOW_AREA = (WIDTH, HEIGHT) = (NUM_X_TILES * TILE_SIZE,
                                 NUM_Y_TILES * TILE_SIZE)

# RGB
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
TRANSPARENT_BLACK = (0, 0, 0, 180)
