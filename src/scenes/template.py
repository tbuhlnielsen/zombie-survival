
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

# ==============================================================================

class Scene:
    """Base class for a scene in the game."""

    def __init__(self, game):
        self.is_running = True
        self.game = game

    def setup(self):
        """Create sprites and sprite groups."""
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
