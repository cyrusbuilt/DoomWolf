import os
import pygame as pg
from typing import Optional

from engine import constants as con


class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface | pg.SurfaceType = game.screen
        wall_tex_path: str = 'assets/textures/walls'
        sky_tex_path: str = 'assets/textures/sky.png'
        blood_screen_path: str = 'assets/textures/blood_screen.png'
        health_digits_path: str = 'assets/textures/digits'
        game_over_path: str = 'assets/textures/game_over.png'
        win_path: str = 'assets/textures/win.png'
        self.wall_textures: Optional[dict] =\
            self.load_wall_textures(wall_tex_path)
        self.sky_image: Optional[pg.Surface | pg.SurfaceType] =\
            self.get_texture(sky_tex_path, (con.WIDTH, con.HALF_HEIGHT))
        self.sky_offset: int = 0
        self.blood_screen: Optional[pg.Surface | pg.SurfaceType] =\
            self.get_texture(blood_screen_path, con.RES)
        self.digit_size: int = 90
        if os.path.exists(health_digits_path):
            self.digit_images = [
                self.get_texture(f'{health_digits_path}/{i}.png',
                                 [self.digit_size] * 2) for i in range(11)
            ]
        else:
            self.digit_images = None
        self.health: Optional[dict] = None
        if self.digit_images and self.digit_images[0]:
            self.health = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image: Optional[pg.Surface | pg.SurfaceType] =\
            self.get_texture(game_over_path, con.RES)
        self.win_image: Optional[pg.Surface | pg.SurfaceType] =\
            self.get_texture(win_path, con.RES)

    @staticmethod
    def get_texture(path: str, res: tuple[int, int] = (con.TEXTURE_SIZE, con.TEXTURE_SIZE))\
            -> Optional[pg.Surface | pg.SurfaceType]:
        if os.path.exists(path):
            if con.DEBUG:
                print(f'Texture path exists: {path}')
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        return None

    def load_wall_textures(self, path: str) -> Optional[dict]:
        if os.path.exists(path):
            textures = {}
            files = os.listdir(path)
            for i in range(len(files)):
                tex_path = f'{path}/{i + 1}.png'
                textures[i + 1] = self.get_texture(tex_path)
            return textures
        return None

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        if self.health:
            health = str(self.game.player.health)
            for i, char in enumerate(health):
                self.screen.blit(self.health[char], (i * self.digit_size, 0))
            self.screen.blit(self.health['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        # TODO background should change with map
        if self.sky_image:
            offset = (self.sky_offset + 4.5 * self.game.player.rel)
            self.sky_offset = offset % con.WIDTH
            self.screen.blit(self.sky_image, (-self.sky_offset, 0))
            self.screen.blit(self.sky_image, (-self.sky_offset + con.WIDTH, 0))
        else:
            self.screen.fill('black')

        # Now, the floor
        rect = (0, con.HALF_HEIGHT, con.WIDTH, con.HEIGHT)
        pg.draw.rect(self.screen, con.FLOOR_COLOR, rect)

    def render_game_objects(self):
        objs_to_render = self.game.ray_caster.objects_to_render
        objects = sorted(objs_to_render, key=lambda t: t[0], reverse=True)
        for unused_depth, image, pos in objects:
            self.screen.blit(image, pos)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
