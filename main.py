"""Zombie survival game

* First written: 14th Feb 2020
* Updated: 21st Feb 2020
  Add effects, use pygame colors.
* Updated: 24th Feb 2020
  Implement scene stack, clean up code slightly.

main - Class for running and controlling the game.
"""

import pygame as pg

from core.scenes.start import StartScene
from core.tools.resources import ResourceLoader

from constants.settings import *


class Game:
    """The scenes in a Game are managed with a stack; this class calls run() on
    the scene on top of the stack, which kicks off an event/update/draw game
    loop.
    """

    def __init__(self):
        """Sets up the game clock, display window and first scene."""
        # load pygame modules
        pg.init()
        pg.mixer.init()

        self.clock = pg.time.Clock()

        self.screen = pg.display.set_mode(WINDOW_AREA)
        self.title = pg.display.set_caption("Zombie Survival")
        self._running = True # set to False to close window

        self._scene = StartScene(self)
        self._stack = [self._scene]

    def get_scene(self):
        return self._scene

    def load(self):
        """Load all the game assets."""
        fx = ResourceLoader(self)

        t1 = pg.time.get_ticks()
        fx.load() # takes about 0.7 seconds
        t2 = pg.time.get_ticks()

        # print("Loading time:", t2 - t1)

    def go_to_scene(self, scene):
        """Stop running the current scene and put a new one at the top of
        the stack.
        """
        self._scene.end()
        self._scene = scene
        self._stack.append(scene)

    def go_to_prev_scene(self):
        """Stop running the current scene and pop it from the top of the stack
        to start running the one below it.
        """
        # don't do anything if the stack only has one element
        if len(self._stack) > 1:
            self._scene.end()
            self._stack.pop()
            self._scene = self._stack[-1]

    def run(self):
        """Call run() on the scene at the top of the stack."""
        while self._running:
            self._scene.run()

    def quit(self):
        """Exits the game."""
        self._running = False

    def __str__(self):
        """Returns a string representation of the scene stack."""

        s = "["

        for i, scene in enumerate(self._stack):
            s += str(scene)
            if i != len(self._stack) - 1:
                s += ", "

        s += "]"

        return s


def main():
    """Loads a game and runs it."""
    g = Game()
    g.load()
    g.run()


if __name__ == "__main__":
    main()
