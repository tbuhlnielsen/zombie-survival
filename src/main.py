
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import scenes.start
import settings

# ==============================================================================

class Game:
    """A zombie survival game."""

    def __init__(self):
        """Initialise pygame, the game clock, and the display window. Retina
        displays require the pg.FULLSCREEN mode to avoid bad frame rates.
        """
        pg.init()
        self.clock = pg.time.Clock()
        self.dt = 0 # duration of a frame
        self.screen = pg.display.set_mode(settings.WINDOW_AREA)
        pg.display.set_caption(settings.CAPTION)

        #--- Choose first scene ---#
        self.active_scene = scenes.start.Level(self)
        #--------------------------#

    def run(self):
        """Set up and run the active scene."""
        while self.active_scene:
            self.active_scene.setup()
            self.active_scene.run()

    def exit(self):
        """Called to quit the game."""
        self.active_scene.is_running = False
        self.active_scene = None

# ==============================================================================

if __name__ == "__main__":
    g = Game()
    g.run()
