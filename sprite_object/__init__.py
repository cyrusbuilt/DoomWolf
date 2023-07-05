import os
import pygame as pg

from engine import constants as con
from game.decorators import copy_method
from sprite_object.door import Door
from sprite_object.door import DoorType


class DoorBuilder:

    def __init__(self, game, path: str, pos: tuple[float, float]):
        self.the_door: Door = Door(game, path, pos)

    @copy_method
    def set_scale_height(self, scale_height: float):
        self.the_door.SPRITE_SCALE = scale_height
        return self

    @copy_method
    def set_scale_width(self, scale_width: float):
        self.the_door.SCALE_WIDTH = scale_width
        return self

    @copy_method
    def set_height_shift(self, shift: float):
        self.the_door.SPRITE_HEIGHT_SHIFT = shift
        return self

    @copy_method
    def set_animation_time(self, animation_time: int):
        self.the_door.animation_time = animation_time
        return self

    @copy_method
    def set_door_type(self, door_type: DoorType):
        self.the_door.type = door_type
        return self

    @copy_method
    def set_interaction_sound(self, sound: pg.mixer.Sound):
        self.the_door.interaction_sound = sound
        return self

    @copy_method
    def set_tile_count(self, tiles: int):
        self.the_door.tile_count = tiles
        return self

    def build(self) -> Door:
        return self.the_door


def door(game, door_dict: dict) -> DoorBuilder:
    name = door_dict.get('name')
    pos_x = door_dict.get('pos_x', 11.0)
    pos_y = door_dict.get('pos_y', 7.5)
    scale_width = door_dict.get('scale_width', 1.0)
    scale_height = door_dict.get('scale_height', 0.8)
    shift = door_dict.get('shift', 0.27)
    anim_time = door_dict.get('animation_time', 120)
    d_type = DoorType(str(door_dict.get('type')))
    sound_file = door_dict.get('interaction_sound')
    tiles = door_dict.get('tiles', 1)

    door_dir = os.path.join(con.DOOR_SPRITE_BASE, name)
    door_path = os.path.join(door_dir, "0.png")
    if os.path.isdir(door_dir):
        files = sorted(os.listdir(door_dir))
        files = [f for f in files if os.path.splitext(f)[1] == '.png']
        door_path = os.path.join(door_dir, files[0])

    pos = (pos_x, pos_y)
    builder: DoorBuilder = DoorBuilder(game, door_path, pos) \
        .set_scale_width(scale_width) \
        .set_scale_height(scale_height) \
        .set_height_shift(shift) \
        .set_animation_time(anim_time) \
        .set_door_type(d_type) \
        .set_tile_count(tiles)

    if sound_file:
        sound_path = os.path.join(con.DOOR_SOUND_BASE, name)
        sound_path = os.path.join(sound_path, sound_file)
        if os.path.exists(sound_path):
            door_sounds = game.sound.get_sprite_sounds(name)
            sound = door_sounds.get(sound_file)
            builder = builder.set_interaction_sound(sound)

    return builder
