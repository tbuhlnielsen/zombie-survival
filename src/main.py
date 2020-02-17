
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import scenes.start
import settings

# ==============================================================================

class Game:
    """A zombie survival game."""

    def __init__(self, display_size=(480, 480), title="Game"):
        """Initialises pygame, the game clock, and the display window."""
        pg.init()

        self.clock = pg.time.Clock()
        self.frame_duration = 0 # will be updated each frame

        self.screen = pg.display.set_mode(display_size)
        self.title = pg.display.set_caption(title)

        #--- Choose first scene ---#
        self.active_scene = scenes.start.Level(self)
        #--------------------------#

    def load_data(self):
        """Load data used in multiple Scenes."""
        self.player_img = fx.load_image("survivor_with_gun.png")
        self.zombie_img = fx.load_image("zombie_hold.png")
        self.bullet_img = fx.load_image("bullet.png")
        self.wall_img = fx.load_image("tile_green.png")


    def run(self):
        """Calls run() on self.active_scene. This kicks off an event/update/draw
        loop that can be terminated by setting the Scene's is_running attribute
        to False. Update self.active_scene after doing so; set to None to end
        the game.
        """
        while self.active_scene:
            self.active_scene.run()

    def exit(self):
        """Quits the game."""
        self.active_scene.is_running = False
        self.active_scene = None

# ==============================================================================

if __name__ == "__main__":
    g = Game(settings.WINDOW_AREA, "Zombie Survival")
    g.load_data()
    g.run()
