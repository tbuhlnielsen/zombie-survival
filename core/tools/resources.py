
"""Zombie survival game

core.tools.resources - Class and functions for loading game assets.

TO DO: add documentation to ResourceLoader and TiledMap.
"""

import pytmx
import pygame as pg

from os import path

from constants.paths import *


# attribute name: [image name, extension]
main_images = {
    "bullet_image": ["bullet", "png"],
    "player_image": ["survivor-with-gun", "png"],
    "zombie_image": ["zombie-hold", "png"],
    "start_background": ["dark-background", "png"]
}

# Item.kind: [image name, extension]
item_images = {
    "health": ["health-pack", "png"]
}

# attribute name: [animation name, extension, number of frames]
main_animations = {
    "smoke_animation": ["gun-smoke", "png", 4],
    "splat_images": ["blood-splats", "png", 5]
}

# attribute name: [sound name, volume]
music_sounds = {
    "background_music": ["espionage.ogg", 0.5],
    "end_screen_music": ["end-screen.ogg", 0.1],
    "start_screen_music": ["start-screen.wav", 1]
}

# attribute name: [sound names, volume]
character_sounds = {
    "zombie_groans": [["zombie-roar-" + str(i) + ".wav" for i in [1, 2, 3, 7, 8]], 0.1],
    "zombie_speech": [["brains2.wav"], 1]
}

# attribute name: [sound name, volume]
gun_sounds = {
    "pistol_sound": ["pistol-shot.ogg", 0.025]
}


def load_image(file_name, extension="png"):
    """Loads the image IMG_DIR/<file_name>.<extension>."""
    full_name = path.join(IMG_DIR, file_name) + "." + extension

    img = pg.image.load(full_name)

    return img.convert_alpha()


def load_animation(file_name, extension_="png", n=1):
    """Loads the images IMG_DIR/<file_name>X.<extension_> for X in range(n)."""
    if n < 0:
        raise ValueError("number of frames must be non-negative")

    full_name = path.join(IMG_DIR, file_name)

    frames = [
        load_image(full_name + str(i), extension=extension_) for i in range(n)
    ]

    return frames


def load_sound(file_name):
    """Loads the sound SOUND_DIR/<file_name>."""
    full_name = path.join(SOUND_DIR, file_name)

    return pg.mixer.Sound(full_name)


def load_font(file_name, size=16):
    """Loads the font FONT_DIR/<file_name>."""
    return pg.font.Font(path.join(FONT_DIR, file_name), size)


class ResourceLoader:
    """A tool for loading assets used in multiple scenes of the game."""

    def __init__(self, game):
        self.game = game

    def load(self):
        self.load_images()
        self.load_animations()
        self.load_sounds()

    def load_images(self):
        # main images
        for a in main_images:
            file_name = main_images[a][0]
            extension = main_images[a][1]
            img = load_image(file_name, extension)
            setattr(self.game, a, img)

        # item images
        self.game.item_images = {}
        for a in item_images:
            file_name = item_images[a][0]
            extension = item_images[a][1]
            img = load_image(file_name, extension)
            self.game.item_images[a] = img

    def load_animations(self):
        # main animations
        for a in main_animations:
            file_name = main_animations[a][0]
            extension = main_animations[a][1]
            n = main_animations[a][2]
            frames = load_animation(file_name, extension, n)
            setattr(self.game, a, frames)

    def load_sounds(self):
        # music
        for a in music_sounds:
            file_name = music_sounds[a][0]
            vol = music_sounds[a][1]
            snd = load_sound(file_name)
            snd.set_volume(vol)
            setattr(self.game, a, snd)

        # character sounds
        for a in character_sounds:
            file_names = character_sounds[a][0]
            vol = character_sounds[a][1]
            setattr(self.game, a, [])

            for f in file_names:
                snd = load_sound(f)
                snd.set_volume(vol)
                getattr(self.game, a).append(snd)

        # gun sounds
        self.game.gun_sounds = {}
        for a in gun_sounds:
            file_name = gun_sounds[a][0]
            vol = gun_sounds[a][1]
            snd = load_sound(file_name)
            snd.set_volume(vol)
            self.game.gun_sounds[a] = snd


class TiledMap:
    """A map created with the Tiled map editor."""

    def __init__(self, file_name):
        """Read data from MAPS_DIR/<file_name>, a tmx file."""
        full_name = path.join(MAPS_DIR, file_name)

        # parts of map are transparent
        self.data = pytmx.load_pygame(full_name, pixelalpha=True)

        # map size
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight
        self.area = (self.width, self.height)

    def render(self, surf):
        """Draw the tiles of self.data onto surf (a pygame surface)."""
        for layer in self.data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.data.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * self.data.tilewidth,
                                         y * self.data.tileheight))

    def get_image(self):
        """TO DO: explain."""
        surf = pg.Surface(self.area)
        self.render(surf)

        return surf
