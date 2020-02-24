
"""Zombie survival game

core.scenes.start - The game's start screen.

TO DO: add documentation and animations?
"""

import pygame as pg

from core.scene import Scene
from core.ui.hud import draw_text

from constants.settings import *


class EndScene(Scene):
    """A demo scene with a blue sprite."""

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

                if event.key == pg.K_BACKSPACE:
                    self.game.go_to_prev_scene()

    def update(self):
        self.dt = self.game.clock.tick(FPS) / 1000 # seconds

    def draw(self):
        self.game.screen.fill(pg.Color("black"))

        draw_text(self.game.screen, "Game Over", size=32)

        pg.display.update()

    def run(self):
        self.game.end_screen_music.play(loops=-1)

        self._running = True
        while self._running:
            self.events()
            self.update()
            self.draw()

    def end(self):
        super().end()
        self.game.end_screen_music.stop()
