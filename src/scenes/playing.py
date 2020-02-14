
"""Zombie survival game

Author: Tom Buhl-Nielsen
First written: 14th Feb 2020

Based on tutorials by KidsCanCode (http://kidscancode.org/).
"""

import pygame as pg

import fx
import scenes.template
import settings
import sprites.mob
import sprites.player
import sprites.wall
import tilemap

# ==============================================================================

class Level(scenes.template.Scene):
    """First level in the game."""

    def setup(self):
        self.all_sprites = pg.sprite.Group() # for drawing
        self.walls = pg.sprite.Group() # for collison detection
        self.mobs = pg.sprite.Group()

        self.map = tilemap.Map("test3.txt")
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == settings.WALL_SYMBOL:
                    w = sprites.wall.Wall(col, row)
                    self.walls.add(w)
                    self.all_sprites.add(w)

                if tile == settings.PLAYER_SYMBOL:
                    self.player = sprites.player.Player(col, row)
                    self.all_sprites.add(self.player)

                if tile == settings.MOB_SYMBOL:
                    m = sprites.mob.Mob(col, row)
                    self.mobs.add(m)
                    self.all_sprites.add(m)

        self.camera = tilemap.Camera(self.map.width, self.map.height)

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.game.exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.is_running = False
                    self.game.active_scene = scenes.start.Level(self.game)

    def update(self):
        self.player.update(self.game.dt, self.walls)
        self.camera.update(self.player)

        for m in self.mobs:
            m.update(self.game.dt, self.walls, self.player)

    def draw(self):
        self.game.screen.fill(settings.RGB_BROWN)

        pg.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))

        # fx.draw_grid(self.game.screen)

        for sprite in self.all_sprites:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.update()

    def run(self):
        while self.is_running:
            self.game.dt = self.game.clock.tick(settings.FPS) / 1000
            self.events()
            self.update()
            self.draw()
