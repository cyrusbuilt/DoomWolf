from enum import Enum
import os
import json

from game.decorators import copy_method


class SpriteType(Enum):
    ANIMATED = 'animated'
    STATIC = 'static'


class SpriteMeta:

    def __init__(self, name: str, pos: tuple[float, float]):
        self.name: str = name
        self.pos_x: float = pos[0]
        self.pos_y: float = pos[1]


class SpriteMap:

    def __init__(self):
        self.static_sprites: list[SpriteMeta] = []
        self.animated_sprites: list[SpriteMeta] = []


class SpriteMapBuilder:

    def __init__(self):
        self.sprite_map: SpriteMap = SpriteMap()

    @copy_method
    def set_static_sprites(self, static_sprites: list[SpriteMeta]):
        self.sprite_map.static_sprites = static_sprites
        return self

    @copy_method
    def set_animated_sprites(self, animated_sprites: list[SpriteMeta]):
        self.sprite_map.animated_sprites = animated_sprites
        return self

    def build(self):
        return self.sprite_map


def sprite_map(path: str) -> SpriteMapBuilder:
    builder = SpriteMapBuilder()
    if os.path.exists(path):
        print(f'Loading sprite map {path} ...')
        with open(path, encoding='UTF-8') as file:
            sprite_map_dict = json.load(file)
            sprites = sprite_map_dict.get('sprites')
            if sprites:
                s_sprites: list[SpriteMeta] = []
                static_sprites = sprites.get(SpriteType.STATIC.value)
                if static_sprites:
                    for s_spr in static_sprites:
                        name = s_spr.get('name')
                        pos_x = s_spr.get('pos_x')
                        pos_y = s_spr.get('pos_y')
                        spr = SpriteMeta(name, (pos_x, pos_y))
                        s_sprites.append(spr)

                    builder.set_static_sprites(s_sprites)

                a_sprites: list[SpriteMeta] = []
                anim_sprites = sprites.get(SpriteType.ANIMATED.value)
                if anim_sprites:
                    for a_spr in anim_sprites:
                        name = a_spr.get('name')
                        pos_x = a_spr.get('pos_x')
                        pos_y = a_spr.get('pos_y')
                        spr = SpriteMeta(name, (pos_x, pos_y))
                        a_sprites.append(spr)

                    builder.set_animated_sprites(a_sprites)
    return builder
