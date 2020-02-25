
"""Zombie survival game

core.scenes.end - The game's end screen.

TO DO: add animations?
"""

import pygame as pg

from core.scene import Scene
from core.ui.hud import draw_text

from constants.settings import *


class EndScene(Scene):
    """The game's end screen."""

    def __init__(self, game):
        super().__init__(game)

    def load(self):
        """Sets up the end screen's music."""
        self.music = self.game.end_screen_music
        self.music.play(loops=-1)

    def events(self):
        """Checks for quitting."""
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.end()
                self.game.end()

    def update(self):
        pass

    def draw(self):
        """Displays a game over message to the player."""
        self.game.screen.fill(BLACK)
        draw_text(self.game.screen, "Game Over", size=48)

    def end(self):
        super().end()
        self.music.stop()
