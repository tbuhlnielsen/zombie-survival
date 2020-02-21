
"""Zombie survival game

core.scenes.start - The game's start screen.
"""

import pygame as pg

from core.ui.hud import draw_text
from constants.settings import Window


class End:
    """Start scene of the game."""

    def __init__(self, game):
        """Get the start scene running."""
        self.game = game
        self.is_running = True

    def setup(self):
        pass

    def events(self):
        """Respond to mouse clicks and key presses."""
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.game.exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.game.end_screen_music.stop()
                    self.game.exit()

    def update(self):
        pass

    def draw(self):
        """Draw the start scene message."""
        self.game.screen.fill(pg.Color("black"))
        draw_text(self.game.screen, "Game Over", size=32)
        pg.display.update()

    def run(self):
        """The main loop."""
        self.game.end_screen_music.play(loops=-1)
        while self.is_running:
            self.game.frame_duration = self.game.clock.tick(Window["fps"]) / 1000
            self.events()
            self.update()
            self.draw()
