
"""Zombie survival game

core.scenes.level - Class representing a level in the game.

TO DO: change occurences of "wall" in .tmx files to "obstacle"
"""

import pygame as pg
import random

from core.scene import Scene
from core.scenes.end import EndScene
from core.sprites.characters import Player, Zombie
from core.sprites.items import Item, Gun
from core.sprites.world import Obstacle
from core.tools.collisions import item_pickup, player_hit, zombies_hit
from core.tools.resources import TiledMap
from core.ui.camera import Camera
from core.ui.hud import draw_text, HUD

from constants.settings import *


class Level(Scene):
    """A level in the game."""

    def __init__(self, game, map_name):
        """Sets up the level's map image, camera, and HUD."""
        super().__init__(game)

        self.map = TiledMap(map_name)
        self.map_image = self.map.get_image()
        self.map_rect = self.map_image.get_rect()

        self.camera = Camera(self.map.width, self.map.height)

        self.hud = HUD(self.game)

        self.debug = False # toggle to show/hide some debugging features

        self.paused = False # toggle to show pause screen
        self.pause_overlay = pg.Surface(self.game.screen.get_size()).convert_alpha()
        self.pause_overlay.fill(TRANSPARENT_BLACK)

    def load_groups(self):
        """Sets up the level's sprite groups. Uses pg.sprite.LayeredUpdates
        instead of pg.sprite.Group so that sprites can be drawn on different
        layers.

        all_sprites: for all sprites actually drawn to screen
        zombies: separate group for detecting collisions with player
        obstacles: for detecting collisions with characters
        items: for items that a player can pick up
        ammo: for detecting collisions with zombies
        """
        groups = [
            "all_sprites",
            "zombies",
            "obstacles",
            "items",
            "ammo"
        ]
        for g in groups:
            setattr(self, g, pg.sprite.LayeredUpdates())

    def load_sprites(self):
        """Loops through a level's map data to set up characters, obstacles, and
        items.
        """
        for tile_obj in self.map.data.objects:
            # tile_obj coordinates are top left of tile
            obj_center = pg.math.Vector2(tile_obj.x + tile_obj.width/2,
                                         tile_obj.y + tile_obj.height/2)

            if tile_obj.name == PLAYER_TILE:
                self.player = Player(self.game, obj_center.x, obj_center.y,
                                      self.game.player_image)

            if tile_obj.name == ZOMBIE_TILE:
                z = Zombie(self.game, obj_center.x, obj_center.y,
                           self.game.zombie_image)

            # DO use top left of tile for obstacles
            if tile_obj.name == OBSTACLE_TILE:
                ob = Obstacle(self.game, tile_obj.x, tile_obj.y, tile_obj.width,
                              tile_obj.height)

            # more items will be added
            if tile_obj.name in [HEALTH_ITEM_TILE]:
                i = Item(self.game, obj_center, tile_obj.name)

    def load(self):
        """Sets up the level's music and sprites."""
        self.music = self.game.background_music
        self.music.play(loops=-1)
        self.load_groups()
        self.load_sprites()

    def events(self):
        """Check for quitting or going to end screen."""
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.end()
                self.game.end()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_h:
                    self.debug = not self.debug

                if e.key == pg.K_p:
                    self.paused = not self.paused

                if e.key == pg.K_RETURN:
                    self.end()
                    self.game.set_scene(EndScene(self.game))

    def update(self):
        """Update all the level's sprites and handle interactions."""
        if self._running and not self.paused:
            self.all_sprites.update()

            self.camera.update(target=self.player)

            # handle collisions
            item_pickup(self.player, self.items)

            zombies_hit(self.zombies, self.ammo, self.player.weapon.damage)
            for z in self.zombies:
                if z.is_dead():
                    z.run_death_sequence()

            player_hit(self.player, self.zombies)
            if self.player.is_dead():
                self.end()
                self.game.set_scene(EndScene(self.game))

    def draw_debug(self):
        """Draw features used for debugging."""
        # hit rects, for debugging collisions
        for sprite in self.all_sprites:
            pg.draw.rect(self.game.screen, CYAN,
                         self.camera.apply_rect(sprite.hit_rect), 2)

        for ob in self.obstacles:
            pg.draw.rect(self.game.screen, CYAN,
                         self.camera.apply_rect(ob.rect), 2)

        # FPS
        frame_rate = "FPS: {:.2f}".format(self.game.clock.get_fps())
        draw_text(self.game.screen, frame_rate, y=20)

    def draw_pause_screen(self):
        """Draws a pause message and dims the screen."""
        self.game.screen.blit(self.pause_overlay, (0, 0))
        draw_text(self.game.screen, "Paused", size=64)

    def draw(self):
        """Draw all the Level's sprites to the game screen."""
        if self._running:
            self.game.screen.blit(self.map_image,
                                  self.camera.apply_rect(self.map_rect))

            for sprite in self.all_sprites:
                if isinstance(sprite, Zombie):
                    sprite.draw_health()
                    # a zombie's health bar is drawn on its image, so this must
                    # come before blitting to the  screen

                self.game.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.debug:
                self.draw_debug()

            if self.paused:
                self.draw_pause_screen()

            self.hud.draw()

    def end(self):
        super().end()
        self.music.stop()
