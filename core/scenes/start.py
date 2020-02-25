
"""Zombie survival game

core.scenes.start - The game's start screen.

TO DO: add menu with highscores, controls, settings.
"""

import pygame as pg

from core.scene import Scene
from core.scenes.level import Level
from core.ui.hud import draw_text

from constants.settings import *


class StartScene(Scene):
    """The game's start screen."""

    def __init__(self, game):
        super().__init__(game)

    def load(self):
        """Sets up the start screen's music and background image."""
        self.music = self.game.start_screen_music
        self.music.play(loops=-1)

        bg = self.game.start_background
        self.background = pg.transform.scale(bg, WINDOW_AREA)

    def events(self):
        """Checks for quitting or starting the game."""
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.end()
                self.game.end()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.end()
                    self.game.set_scene(Level(self.game, "demo.tmx"))

    def update(self):
        pass

    def draw(self):
        """Displays a message telling the player to start the game."""
        self.game.screen.blit(self.background, (0, 0))
        draw_text(self.game.screen, "Press Enter", size=48)

    def end(self):
        """Stops the start screen's music playing."""
        super().end()
        self.music.stop()
