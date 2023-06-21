from collections import deque
import copy
import json
import os
import pygame as pg
from enum import Enum

from engine import constants as con
from engine.weapon import Weapon


def copy_method(method):
    def _inner(self, *args, **kwargs):
        clone = copy.copy(self)
        method(clone, *args, **kwargs)
        return clone

    return _inner


class WeaponBuilder:

    def __init__(self, game, path: str):
        self.the_weapon: Weapon = Weapon(game, path)

    @copy_method
    def set_name(self, name: str):
        self.the_weapon.name = name
        return self

    @copy_method
    def set_has_continuous_fire(self, has_cont_fire: bool):
        self.the_weapon.has_continuous_fire = has_cont_fire
        return self

    @copy_method
    def set_damage(self, damage: int):
        self.the_weapon.damage = damage
        return self

    @copy_method
    def set_scale(self, scale: float):
        self.the_weapon.SPRITE_SCALE = scale
        return self

    @copy_method
    def set_ammo_capacity(self, capacity: int):
        self.the_weapon.ammo_capacity = capacity
        return self

    @copy_method
    def set_ammo_use(self, ammo_use: int):
        self.the_weapon.ammo_use = ammo_use
        return self

    @copy_method
    def set_magazine_capacity(self, mag_cap: int):
        self.the_weapon.magazine_capacity = mag_cap
        return self

    @copy_method
    def set_sounds(self, sounds: dict[str, pg.mixer.Sound]):
        self.the_weapon.sounds = sounds
        return self

    @copy_method
    def set_animation_frames(self, frames: dict[str, str]):
        # TODO Not sure if we should keep this or not. We need this
        # temporarily for sure until we can define custom action
        # animations, etc. But on the other hand, this might be
        # nice to have regardless since it gives a good fall back.
        if frames:
            name = self.the_weapon.name
            img_dir = os.path.join(con.WEAPON_SPRITE_BASE, name)
            the_frames = dict(sorted(frames.items()))
            the_frames = {k: os.path.join(img_dir, the_frames[k])
                          for k in the_frames.keys()}
            self.the_weapon.animation_frames = {
                k: pg.image.load(the_frames[k]).convert_alpha()
                for k in the_frames.keys()
            }

            self.the_weapon.images = deque(
                [*self.the_weapon.animation_frames.values()])

        # TODO Duplicated from weapon.py, move to some kind of model update
        if self.the_weapon.image:
            scale = self.the_weapon.SPRITE_SCALE
            s_w = self.the_weapon.image.get_width() * scale
            s_h = self.the_weapon.image.get_height() * scale
            self.the_weapon.images = deque([
                pg.transform.smoothscale(img, (s_w, s_h))
                for img in self.the_weapon.images
            ])
            self.the_weapon.num_images = len(self.the_weapon.images)
            i_w = con.HALF_WIDTH - self.the_weapon.images[0].get_width() // 2
            i_h = con.HEIGHT - self.the_weapon.images[0].get_height()
            self.the_weapon.weapon_pos = (i_w, i_h)

        return self

    @property
    def assembled(self):
        # NOTE: If needed, we can call any additional initialization logic here
        return self.the_weapon


def weapon(game, data_path: str) -> WeaponBuilder:
    if os.path.exists(data_path):
        with open(data_path, encoding='UTF-8') as file:
            weapon_dict = json.load(file)
            name = weapon_dict.get('name')
            # TODO Error if no name?

            img_path = None
            img = weapon_dict.get('image')
            if img:
                img_dir = os.path.join(con.WEAPON_SPRITE_BASE, name)
                path = os.path.join(img_dir, img)
                if os.path.exists(path):
                    img_path = path

            cont_fire = weapon_dict.get('has_continuous_fire', False)
            dmg = weapon_dict.get('damage', 50)
            scale = weapon_dict.get('scale', 0.4)
            ammo_cap = weapon_dict.get('ammo_capacity', 20)
            ammo_use = weapon_dict.get('ammo_use', 1)
            mag_cap = weapon_dict.get('magazine_capacity', 0)

            sounds: dict[str, pg.mixer.Sound] = {}
            action_sounds = weapon_dict.get('action_sounds')
            if action_sounds:
                weapon_sounds = game.sound.get_weapon_sounds(name)
                for action in action_sounds.keys():
                    action_file = action_sounds[action]
                    if action_file in weapon_sounds:
                        sounds[action] = weapon_sounds.get(action_file)

            frames: dict[str, pg.Surface] = {}
            animation_frames = weapon_dict.get('animation_frames')
            if animation_frames:
                frames = animation_frames

            # TODO Also need a way to load an animation sequence
            # Ideally, something similar to ZDoom, where we can
            # define a sequence where you specify: frame, ticks, action
            # ie: "A", 3, "play_sound('fire')" or something like that

            builder = WeaponBuilder(game, img_path) \
                .set_name(name) \
                .set_has_continuous_fire(cont_fire) \
                .set_damage(dmg) \
                .set_scale(scale) \
                .set_ammo_capacity(ammo_cap) \
                .set_ammo_use(ammo_use) \
                .set_magazine_capacity(mag_cap) \
                .set_sounds(sounds) \
                .set_animation_frames(frames)

            return builder


# TODO this is deprecated once the new weapon system is fully implemented.
class WeaponClass(Enum):
    PISTOL = 'pistol'
    SHOTGUN = 'shotgun'
    CHAINSAW = 'chainsaw'
    SUPER_SHOTGUN = 'super_shotgun'
    CHAIN_GUN = 'chain_gun'
    NONE = 'none'


# TODO This is deprecated once the new weapon system is fully implemented.
class WeaponBase(Weapon):
    # TODO Need to completely rethink this. Instead of adding new members
    # to the enum and making new subclasses for each new type of weapon,
    # maybe just have the generic weapon class support all variables,
    # event hooks, etc and then declare it's type as string (for unique
    # identification and to help locate assets) and then load all the
    # variables from a JSON file. This will making modding easier and
    # make introducing new weapons as easy as writing a new JSON file.
    # We'll keep using the existing system for now though to help determine
    # what all needs to go into the JSON schema.

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class: WeaponClass = WeaponClass.NONE
