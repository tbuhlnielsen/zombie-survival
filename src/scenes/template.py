
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

# ==============================================================================

class Scene:
    """Base class for a scene in the game."""

    def __init__(self, game):
        self.is_running = True
        self.game = game

    def setup_groups(self, *args):
        """Set up sprite groups for a Scene."""
        for group in args:
            setattr(self, group, pg.sprite.Group())

    def setup(self):
        """Set up sprites for a Scene."""
        raise NotImplementedError

    def events(self):
        """Listen for key/mouse events."""
        raise NotImplementedError

    def update(self):
        """Update the attributes of a Scene's sprites in response to events."""
        raise NotImplementedError

    def draw(self):
        """Draw a Scene's sprites to a screen."""
        raise NotImplementedError

    def run(self):
        """The main loop."""
        raise NotImplementedError
