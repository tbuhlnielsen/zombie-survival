
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import scenes.template
import scenes.playing
import settings

# ==============================================================================

class Level(scenes.template.Scene):
    """Start scene of the game."""

    def setup(self):
        pass

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.game.exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.is_running = False
                    self.game.active_scene = scenes.playing.Level(self.game)

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill(settings.RGB_BLACK)

        fx.draw_text(self.game.screen, "Press enter to start")

        pg.display.update()

    def run(self):
        while self.is_running:
            self.game.dt = self.game.clock.tick(settings.FPS) / 1000
            self.events()
            self.update()
            self.draw()
