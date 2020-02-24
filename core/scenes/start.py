
"""Zombie survival game

core.scenes.start - The game's start screen.

TO DO: add documentation and animations?
"""

import pygame as pg

from core.scene import Scene
from core.scenes.level import Level
from core.ui.hud import draw_text

from constants.settings import *


class StartScene(Scene):
    """The welcome screen of the game."""

    def __init__(self, game):
        super().__init__(game)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.end()
                self.game.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.end()
                    self.game.quit()

                if event.key == pg.K_RETURN:
                    self.game.go_to_scene(Level(self.game, "demo"))

                if event.key == pg.K_BACKSPACE:
                    self.game.go_to_prev_scene()

    def update(self):
        self.dt = self.game.clock.tick(FPS) / 1000 # seconds

    def draw(self):
        self.game.screen.fill(pg.Color("black"))

        draw_text(self.game.screen, "Press Enter", size=32)

        pg.display.update()

    def run(self):
        self.game.start_screen_music.play(loops=-1)

        self._running = True
        while self._running:
            self.events()
            self.update()
            self.draw()

    def end(self):
        super().end()
        self.game.start_screen_music.stop()
