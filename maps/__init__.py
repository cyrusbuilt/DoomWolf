import json
import os
import pygame as pg
from typing import Optional

from engine import constants as con
from engine.map import Map
from game.decorators import copy_method


class MapBuilder:

    def __init__(self, game, name: str):
        self.the_map: Map = Map(game, name)

    @copy_method
    def set_mini_map(self, mini_map: list[list[int]]):
        self.the_map.mini_map = mini_map
        return self

    @copy_method
    def set_sky_texture(self, sky: pg.Surface):
        self.the_map.sky_texture = sky
        return self

    @copy_method
    def set_sky_offset(self, offset: int):
        self.the_map.sky_offset = offset
        return self

    @copy_method
    def set_floor_texture(self, floor: pg.Surface):
        self.the_map.floor_texture = floor
        return self

    @copy_method
    def set_floor_color(self, color: pg.Color):
        self.the_map.floor_color = color
        return self

    @copy_method
    def set_music_track(self, track_file: str):
        self.the_map.music_track = track_file
        return self

    @copy_method
    def set_sprite_map_path(self, path: str):
        self.the_map.sprite_map_path = path
        return self

    @copy_method
    def set_enemy_count(self, enemy_count: int):
        self.the_map.enemy_count = enemy_count
        return self

    @copy_method
    def set_enemies(self, enemies: Optional[list[str]] = None):
        self.the_map.enemies = enemies
        return self

    def build(self) -> Map:
        self.the_map.load_map()
        return self.the_map


def game_map(game, map_path: str) -> MapBuilder:
    if os.path.exists(map_path):
        print(f'Loading map {map_path} ...')
        with open(map_path, encoding='UTF-8') as file:
            map_dict = json.load(file)

            name = map_dict.get('name')
            music = map_dict.get('music', 'theme.mp3')
            sky_tex = map_dict.get('sky_texture', 'sky.png')
            floor_tex = map_dict.get('floor_texture')
            floor_clr = map_dict.get('floor_color',
                                     {'R': 30, 'G': 30, 'B': 30})
            mini_map = map_dict.get('minimap')
            sprite_map = map_dict.get('sprite_map')
            enemy_count = map_dict.get('enemy_count', 20)
            enemies = map_dict.get('enemies')

            builder: MapBuilder = MapBuilder(game, name) \
                .set_mini_map(mini_map) \
                .set_floor_texture(floor_tex) \
                .set_enemy_count(enemy_count) \
                .set_enemies(enemies)

            music_path = os.path.join(con.MUSIC_BASE, music)
            if os.path.exists(music_path):
                builder = builder.set_music_track(music_path)

            sky_tex_path = os.path.join(con.TEXTURE_BASE, sky_tex)
            if os.path.exists(sky_tex_path):
                sky_res = (con.WIDTH, con.HALF_HEIGHT)
                the_sky = game.object_renderer.get_texture(sky_tex_path, sky_res)
                if the_sky:
                    builder = builder.set_sky_texture(the_sky)

            if floor_clr:
                flr_clr = pg.Color((
                    floor_clr['R'], floor_clr['G'], floor_clr['B']))
                builder = builder.set_floor_color(flr_clr)

            if sprite_map:
                map_dir = os.path.join(con.MAP_DATA_BASE, name)
                sm_full_path = os.path.join(map_dir, sprite_map)
                builder = builder.set_sprite_map_path(sm_full_path)

            return builder
