
"""Zombie survival game

core.scenes.level - Class representing a level in the game.

TO DO: change occurences of "wall" in .tmx files to "obstacle"
"""

import pygame as pg

from core.scenes.end import End

from constants.settings import Window

from core.sprites.characters import Player, Zombie
from core.sprites.items import Item
from core.sprites.world import Obstacle

from core.tools.collisions import collide_hit_rect

from core.ui.camera import Camera
from core.ui.hud import HUD
from core.ui.tilemap import TiledMap


class Level:
    """A level in the game."""

    def __init__(self, game, map_name):
        """Get a Level running.

        Toggle self.debug to show/hide some useful debugging features.
        """
        self.game = game
        self.map_name = map_name

        self.is_running = True
        self.debug = False

    def load_map(self):
        """Loads the Level's map."""
        self.map = TiledMap(self.map_name)
        self.map_img = self.map.make()
        self.map_rect = self.map_img.get_rect()

    def load_groups(self):
        """Set up sprite groups for a Level."""
        for group in ["all_sprites", "zombies", "obstacles", "bullets", "items"]:
            setattr(self, group, pg.sprite.LayeredUpdates())

    def load_sprites(self):
        """Loads a Level's sprites."""
        for tile_obj in self.map.data.objects:
            obj_center = pg.math.Vector2(tile_obj.x + tile_obj.width/2,
                                         tile_obj.y + tile_obj.height/2)

            if tile_obj.name == "player":
                self.player = Player(self.game, obj_center.x, obj_center.y,
                                      self.game.player_img)

            if tile_obj.name == "zombie":
                z = Zombie(self.game, obj_center.x, obj_center.y,
                           self.game.zombie_img)

            if tile_obj.name == "wall":
                ob = Obstacle(self.game, tile_obj.x, tile_obj.y, tile_obj.width,
                              tile_obj.height)

            if tile_obj.name in ["health"]: # ADD MORE ITEMS
                i = Item(self.game, obj_center, tile_obj.name)

    def setup(self):
        """Load everything needed to get a Level ready."""
        self.load_map()
        self.load_groups()
        self.load_sprites()
        self.camera = Camera(self.map.width, self.map.height)
        self.hud = HUD(self.game)

    def events(self):
        """Respond to mouse clicks and key presses."""
        if self.game.active_scene:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.game.exit()

                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_h:
                        self.debug = not self.debug

    def update(self):
        """Update all the Level's sprites and handle interactions."""
        if self.game.active_scene:
            self.all_sprites.update()

            self.camera.update(target=self.player)

            items = self.player.check_item_pickup()
            for i in items:
                if i.kind == "health" and self.player.health < self.player.max_health:
                    i.kill()
                    self.player.add_health(50)


            # Check for weapons hitting zombies.
            hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
            for hit in hits:
                hit.health -= self.player.weapon.damage
                hit.velocity = pg.math.Vector2(0, 0) # Zombie stops moving when
                                                     # hit.

            # Check for zombies hitting player.
            hits = pg.sprite.spritecollide(self.player, self.zombies, False,
                                           collide_hit_rect)
            for hit in hits:
                self.player.health -= 10
                hit.velocity = pg.math.Vector2(0, 0) # Zombie stops moving when
                                                     # it hits player.
                if self.player.health <= 0:
                    self.game.background_music.stop()
                    self.is_running = False
                    self.game.active_scene = End(self.game)

            if hits:
                self.player.position += pg.math.Vector2(20, 0).rotate(-hits[0].rotation)

    def draw_debug(self):
        """Draw features used for debugging."""
        # hit rects
        for sprite in self.all_sprites:
            pg.draw.rect(self.game.screen, pg.Color("cyan"),
                         self.camera.apply_rect(sprite.hit_rect), 2)

        for ob in self.obstacles:
            pg.draw.rect(self.game.screen, pg.Color("cyan"),
                         self.camera.apply_rect(ob.rect), 2)

    def draw(self):
        """Draw all the Level's sprites to the game screen."""
        if self.is_running:
            title = "FPS: {:.2f}".format(self.game.clock.get_fps())
            pg.display.set_caption(title)

            self.game.screen.blit(self.map_img,
                                  self.camera.apply_rect(self.map_rect))

            for sprite in self.all_sprites:
                if isinstance(sprite, Zombie):
                    sprite.draw_health() # This must come before sprite blitting
                                         # in order for the health bar to
                                         # actually be drawn.

                self.game.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.debug:
                self.draw_debug()

            self.hud.draw()

            pg.display.update()

    def run(self):
        """The main loop."""
        self.game.background_music.play(loops=-1)
        while self.is_running:
            self.game.frame_duration = self.game.clock.tick(Window["fps"]) / 1000
            self.events()
            self.update()
            self.draw()
