
"""Zombie survival game

constants.settings - Constants defining some global game settings.
"""

# Layers
Layer = {
    "obstacle": 1,
    "item": 1,
    "character": 2,
    "weapon": 3,
    "effects": 4
}

# Tiles
Tile = {
    "size": 32, # pixels
    "area": (32, 32),
    "num_x": 32,
    "num_y": 24
}

# Window
Window  = {
    "fps": 60,
    "width": Tile["num_x"] * Tile["size"],
    "height": Tile["num_y"] * Tile["size"],
    "area": (Tile["num_x"] * Tile["size"], Tile["num_y"] * Tile["size"]),
    "caption": "Zombie Survival"
}
