import os
import pygame as pg
from typing import Optional

from engine import constants as con


class ObjectRenderer:

    def __init__(self, game):
        self.game = game
        self.screen: pg.Surface = game.screen
        self.wall_textures: Optional[dict] = None
        self.sky_image: Optional[pg.Surface] = None
        self.sky_offset: int = 0
        self.blood_screen: Optional[pg.Surface] = None
        # TODO Health display is in the HUD now.
        # self.digit_size: int = 90
        # self.digit_images: Optional[list[pg.Surface]] = None
        self.health: Optional[dict] = None
        self.game_over_image: Optional[pg.Surface] = None
        self.win_image: Optional[pg.Surface] = None
        self.floor_color: pg.Color = pg.Color(con.DEFAULT_FLOOR_COLOR)
        # TODO Need to support a floor texture

    def setup(self):
        self.wall_textures = self.load_wall_textures(con.WALL_TEXTURE_BASE)
        if self.sky_image is None:
            sky_tex_path: str = os.path.join(con.TEXTURE_BASE, 'sky.png')
            res = (con.WIDTH, con.HALF_HEIGHT)
            self.sky_image = self.get_texture(sky_tex_path, res)

        blood_screen_path: str = os.path.join(con.TEXTURE_BASE, 'blood_screen.png')
        self.blood_screen = self.get_texture(blood_screen_path, con.RES)

        # TODO Health display is in the HUD now. Remove this but maybe keep assets for future use?
        # health_digits_path: str = con.DIGITS_TEXTURE_BASE
        # self.digit_images = None
        # if os.path.exists(health_digits_path):
        #     self.digit_images = [
        #         self.get_texture(f'{health_digits_path}/{i}.png',
        #                         [self.digit_size] * 2) for i in range(11)
        #     ]
        #
        # if self.digit_images and self.digit_images[0]:
        #     self.health = dict(zip(map(str, range(11)), self.digit_images))

        game_over_path: str = os.path.join(con.TEXTURE_BASE, 'game_over.png')
        self.game_over_image = self.get_texture(game_over_path, con.RES)

        win_path: str = os.path.join(con.TEXTURE_BASE, 'win.png')
        self.win_image = self.get_texture(win_path, con.RES)

    @staticmethod
    def get_texture(path: str, res: tuple[int, int] = (con.TEXTURE_SIZE, con.TEXTURE_SIZE))\
            -> Optional[pg.Surface | pg.SurfaceType]:
        if os.path.exists(path):
            if con.DEBUG:
                print(f'Texture path exists: {path}')
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        return None

    def load_wall_textures(self, path: str) -> Optional[dict[int, pg.Surface]]:
        if os.path.exists(path):
            textures = {}
            files = os.listdir(path)
            for i in range(len(files)):
                tex_path = f'{path}/{i + 1}.png'
                textures[i + 1] = self.get_texture(tex_path)
            return textures
        return None

    def win(self):
        if self.win_image:
            self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        if self.game_over_image:
            self.screen.blit(self.game_over_image, (0, 0))

    # TODO Health display is in the HUD now.
    # def draw_player_health(self):
    #     if self.health:
    #         health = str(self.game.player.health)
    #         for i, char in enumerate(health):
    #             self.screen.blit(self.health[char], (i * self.digit_size, 0))
    #         self.screen.blit(self.health['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        if self.blood_screen:
            self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        if self.sky_image:
            offset = (self.sky_offset + 4.5 * self.game.player.rel)
            self.sky_offset = offset % con.WIDTH
            self.screen.blit(self.sky_image, (-self.sky_offset, 0))
            self.screen.blit(self.sky_image, (-self.sky_offset + con.WIDTH, 0))
        else:
            self.screen.fill('black')

        # Now, the floor
        # TODO Prefer floor texture if defined, over floor color
        # TODO Fallback to default floor color if neither defined.
        rect = (0, con.HALF_HEIGHT, con.WIDTH, con.HEIGHT)
        pg.draw.rect(self.screen, self.floor_color, rect)

    def render_game_objects(self):
        objs_to_render = self.game.ray_caster.objects_to_render
        objects = sorted(objs_to_render, key=lambda t: t[0], reverse=True)
        for unused_depth, image, pos in objects:
            self.screen.blit(image, pos)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        # TODO Health display is in the HUD now.
        # self.draw_player_health()
