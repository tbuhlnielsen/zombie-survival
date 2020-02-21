
"""Zombie survival game

Author: Tom Buhl-Nielsen

* First written: 14th Feb 2020
* Updated: 21st Feb 2020
  Add effects, use pygame colors.

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

from constants.settings import Window
from core.scenes.start import Start
from core.tools.loadresource import ResourceLoader


class Game:
    """A zombie survival game."""

    def __init__(self, display_size=Window["area"], title=Window["caption"]):
        """Initialises pygame, the game clock, and the display window."""
        pg.init()
        pg.mixer.init()

        self.clock = pg.time.Clock()
        self.frame_duration = 0 # will be updated each frame

        self.screen = pg.display.set_mode(display_size)
        self.title = pg.display.set_caption(title)

        #--- Choose first scene ---#
        self.active_scene = Start(self)
        #--------------------------#

        self.fx = ResourceLoader(self)
        self.fx.load()

    def run(self):
        """Kicks off an event/update/draw loop that can be terminated by setting
        the active_scene's is_running attribute to False. Update the
        active_scene after doing so, or set to None to end the game.
        """
        while self.active_scene:
            self.active_scene.setup()
            self.active_scene.run()

    def exit(self):
        """Quits the game."""
        self.active_scene.is_running = False
        self.active_scene = None


def main():
    """Make and run the game."""
    g = Game()
    g.run()


if __name__ == "__main__":
    main()
