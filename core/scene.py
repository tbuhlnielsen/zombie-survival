
"""Zombie survival game

core.scene - Base class for a scene in the game.
"""

import pygame as pg

from constants.settings import *


class Scene:
    """Base class for a scene in the game."""

    def __init__(self, game):
        self.game = game

    def load(self):
        """Additional set up for the scene, e.g. reset score to 0 or start
        playing background music.
        """
        raise NotImplementedError

    def events(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def run(self):
        """Runs the main loop."""
        self._running = True
        while self._running:
            self.dt = self.game.clock.tick(FPS) / 1000 # seconds
            self.events()
            self.update()
            self.draw()
            pg.display.update()

    def end(self):
        """Breaks out of the main loop. This method is intended to be extended
        with commands to terminate processes (such as background music) before
        moving to another scene.
        """
        self._running = False

    def __str__(self):
        """Returns the name of this class (or a subclass) as a string."""
        return type(self).__name__
