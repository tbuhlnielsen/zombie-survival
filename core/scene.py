
"""Zombie survival game

core.scene
"""

import pygame as pg


class Scene:
    """Base class for a scene in the game."""

    def __init__(self, game):
        self.game = game

    def events(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def run(self):
        """Main loop."""
        raise NotImplementedError

    def end(self):
        """Breaks out of the main loop. Extend in a subclass to kill processes
        specific to self before moving to next scene.
        """
        self._running = False

    def __str__(self):
        """Returns the name of this class (or a subclass) as a string."""
        return type(self).__name__
