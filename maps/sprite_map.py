from enum import Enum
import os
import json

from game.decorators import copy_method
from sprite_object import door
from sprite_object import item
from sprite_object.door import Door
from sprite_object.item import Item


class SpriteType(Enum):
    ANIMATED = 'animated'
    STATIC = 'static'
    DOOR = 'door'
    ITEM = 'item'


class SpriteMeta:

    def __init__(self, name: str, pos: tuple[float, float]):
        self.name: str = name
        self.pos_x: float = pos[0]
        self.pos_y: float = pos[1]


class SpriteMap:

    def __init__(self):
        self.static_sprites: list[SpriteMeta] = []
        self.animated_sprites: list[SpriteMeta] = []
        self.door_sprites: list[Door] = []
        self.item_sprites: list[Item] = []


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

    @copy_method
    def set_door_sprites(self, door_sprites: list[Door]):
        self.sprite_map.door_sprites = door_sprites
        return self

    @copy_method
    def set_item_sprites(self, item_sprites: list[Item]):
        self.sprite_map.item_sprites = item_sprites
        return self

    def build(self):
        return self.sprite_map


def sprite_map(game, path: str) -> SpriteMapBuilder:
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

                d_sprites: list[Door] = []
                door_sprites = sprites.get(SpriteType.DOOR.value)
                if door_sprites:
                    for d_spr in door_sprites:
                        the_door = door(game, d_spr).build()
                        d_sprites.append(the_door)

                    builder.set_door_sprites(d_sprites)

                i_sprites: list[Item] = []
                item_sprites = sprites.get(SpriteType.ITEM.value)
                if item_sprites:
                    for i_spr in item_sprites:
                        the_item = item(game, i_spr).build()
                        i_sprites.append(the_item)

                    builder.set_item_sprites(i_sprites)
    return builder
