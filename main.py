"""Zombie survival game

* First written: 14th Feb 2020

* Updated: 21st Feb 2020
  Add effects, use pygame colors.

* Updated: 24th Feb 2020
  Implement scene stack, clean up code slightly.

* Updated: 25th Feb 2020
  Continue code clean-up, add pause screen, remove scene stack.

main - Class for running and controlling the game.
"""

import pygame as pg

from core.scenes.start import StartScene
from core.tools.resources import ResourceLoader

from constants.settings import *


class Game:
    """A zombie survival game."""

    def __init__(self):
        """Sets up the game clock, display window and first scene."""
        # load pygame modules
        # pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        pg.mixer.init()

        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode(WINDOW_AREA)
        self.title = pg.display.set_caption(TITLE)

        self._scene = StartScene(self)

    def get_scene(self):
        """Returns the active scene."""
        return self._scene

    def set_scene(self, scene):
        """Updates the current scene to a new one."""
        self._scene = scene

    def load(self):
        """Loads all the game assets. Returns the time taken to do so."""
        fx = ResourceLoader(self)

        t1 = pg.time.get_ticks()
        fx.load()
        t2 = pg.time.get_ticks()

        return t2 - t1 # loading time - about 700 milliseconds

    def run(self):
        """Continuously runs the active scene."""
        self._open = True # set to False to close window
        while self._open:
            self._scene.load()
            self._scene.run()

    def end(self):
        """Exits the game."""
        self._open = False


def main():
    """Loads a game and runs it."""
    game = Game()
    game.load()
    game.run()
    pg.quit()


if __name__ == "__main__":
    main()
