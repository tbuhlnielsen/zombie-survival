
"""Zombie survival game

core.tools.loadresource - Class and functions for loading game assets.
"""

import pygame as pg

from os import path

from constants.paths import ANIMATION_DIR, IMG_DIR, MUSIC_DIR, SOUND_DIR


def load_image(file_name, extension="png"):
    """Loads the image IMG_DIR/<file_name>.<extension>."""
    full_name = path.join(IMG_DIR, file_name) + "." + extension
    img = pg.image.load(full_name)
    return img.convert_alpha()


def load_animation(file_name, extension_="png", num_frames=0):
    """Loads the images ANIMATION_DIR/<file_name>X.<extension> for X in the
    range 0, 1, ..., num_frames - 1.
    """
    if num_frames < 0:
        raise ValueError("num_frames must be non-negative")

    full_name = path.join(ANIMATION_DIR, file_name)

    frames = []

    for i in range(num_frames):
        frame = full_name + str(i)
        frames.append(load_image(frame, extension=extension_))

    return frames


def load_sound(file_name, extension="wav"):
    """Loads the sound SOUND_DIR/<file_name>.<extension>."""
    full_name = path.join(SOUND_DIR, file_name) + "." + extension
    return pg.mixer.Sound(full_name)


def load_music(file_name, extension="wav"):
    """Loads the sound MUSIC_DIR/<file_name>.<extension>."""
    full_name = path.join(MUSIC_DIR, file_name) + "." + extension
    return pg.mixer.Sound(full_name)


class ResourceLoader:
    """A tool for loading assets used in multiple scenes of the game."""

    def __init__(self, game):
        self.game = game

    def load(self):
        """Load all the data."""
        self.load_images()
        self.load_animations()
        self.load_audio()

    def load_images(self):
        # character images
        self.game.player_img = load_image("survivor-with-gun")
        self.game.zombie_img = load_image("zombie-hold")
        self.game.bullet_img = load_image("bullet")

        # item images
        items = {
            "health": "health-pack" # Item.kind: image file name
        }
        self.game.item_imgs = {}
        for i in items:
            self.game.item_imgs[i] = load_image(items[i])

    def load_animations(self):
        self.game.gun_animation = load_animation("gun-smoke", num_frames=4)

    def load_audio(self):
        # music
        self.game.start_screen_music = load_music("start-screen")

        self.game.background_music = load_music("espionage", extension="ogg")

        self.game.end_screen_music = load_music("end-screen", extension="ogg")
        self.game.end_screen_music.set_volume(0.1)

        # effects
        zombie_groans = [
            "zombie-roar-1", "zombie-roar-2", "zombie-roar-3", "zombie-roar-7",
            "zombie-roar-8", "brains2"
        ]
        self.game.zombie_sound_effects = []
        for s in zombie_groans:
            effect = load_sound(s)
            effect.set_volume(0.1)
            self.game.zombie_sound_effects.append(effect)

        gun_sounds = {
            "pistol": ["pistol-shot", "ogg"] # Gun sub-class: [audio file name, extension]
        }
        self.game.gun_sound_effects = {}
        for s in gun_sounds:
            effect = load_sound(gun_sounds[s][0], extension=gun_sounds[s][1])
            effect.set_volume(0.025)
            self.game.gun_sound_effects[s] = effect

        # self.zombie_death_effect = fx.load_sound("shade12")
