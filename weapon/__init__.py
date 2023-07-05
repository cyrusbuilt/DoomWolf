from collections import deque
import json
import os
import pygame as pg

from engine import constants as con
from engine.weapon import Weapon
from game.decorators import copy_method


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

        return self

    def build(self) -> Weapon:
        # NOTE: If needed, we can call any additional initialization logic here
        self.the_weapon.setup()
        return self.the_weapon


def weapon(game, data_path: str) -> WeaponBuilder:
    if os.path.exists(data_path):
        print(f'Loading weapon descriptor {data_path} ...')
        with open(data_path, encoding='UTF-8') as file:
            weapon_dict = json.load(file)
            # TODO we probably want some additional parser/validation logic
            # here to validate the JSON file. Ideally, we don't want the game
            # to crash when loading these. We're better off using sane defaults
            # for missing values where we can and anything we can't (like assets)
            # then we should throw an exception that gets handled further up the
            # stack and reject the JSON file altogether. Better to have a weapon
            # that doesn't behave or render right or doesn't load at all, than
            # to crash the game. Also, we should probably have a default embedded
            # weapon of some kind (fists? pistol?) that can't be removed so that
            # if no weapon descriptors are found at startup, we can throw a
            # non-fatal error or warning indicating such, but the game can still
            # launch and the user can still play albeit with only one weapon.
            # Probably want to do the same thing with maps, power-ups, enemies,
            # etc.

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

            frames: dict[str, str] = {}
            animation_frames = weapon_dict.get('animation_frames')
            if animation_frames:
                frames = animation_frames

            # TODO Also need a way to load an animation sequence
            # Ideally, something similar to ZDoom, where we can
            # define a sequence where you specify: frame, ticks, action
            # ie: "A", 3, "play_sound('fire')" or something like that

            builder: WeaponBuilder = WeaponBuilder(game, img_path) \
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
