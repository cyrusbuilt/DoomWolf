import os
import json
import pygame as pg
from random import randint
from typing import Optional

from engine import constants as con
from engine.enemy import Enemy
from game.decorators import copy_method


class EnemyBuilder:

    def __init__(self, game, path: str, pos: tuple[float, float]):
        self.the_enemy: Enemy = Enemy(game, path, pos)

    @copy_method
    def set_name(self, name: str):
        self.the_enemy.name = name
        return self

    @copy_method
    def set_scale(self, scale: float):
        self.the_enemy.SPRITE_SCALE = scale
        return self

    @copy_method
    def set_shift(self, shift: float):
        self.the_enemy.SPRITE_HEIGHT_SHIFT = shift
        return self

    @copy_method
    def set_animation_time(self, time: int):
        self.the_enemy.animation_time = time
        return self

    @copy_method
    def set_speed(self, speed: float):
        self.the_enemy.speed = speed
        return self

    @copy_method
    def set_size(self, size: int):
        self.the_enemy.size = size
        return self

    @copy_method
    def set_attack_distance(self, distance: int):
        self.the_enemy.attack_dist = distance
        return self

    @copy_method
    def set_health(self, health: int):
        self.the_enemy.health = health
        return self

    @copy_method
    def set_attack_damage(self, damage: int):
        self.the_enemy.attack_damage = damage
        return self

    @copy_method
    def set_accuracy(self, accuracy: float):
        self.the_enemy.accuracy = accuracy
        return self

    @copy_method
    def set_sounds(self, sounds: dict[str, pg.mixer.Sound]):
        attack_sound = sounds.get('attack')
        if attack_sound:
            attack_sound.set_volume(0.2)

        self.the_enemy.sounds = sounds
        return self

    @copy_method
    def set_spawn_weight(self, weight: int):
        self.the_enemy.spawn_weight = weight
        return self

    def build(self) -> Enemy:
        self.the_enemy.setup()
        return self.the_enemy


def enemy(game, data_path: str, pos: tuple[float, float]) -> EnemyBuilder:
    if os.path.exists(data_path):
        print(f'Loading enemy descriptor {data_path} ...')
        with open(data_path, encoding='UTF-8') as file:
            enemy_dict = json.load(file)
            name = enemy_dict.get('name')

            img_path = None
            img = enemy_dict.get('image')
            if img:
                img_dir = os.path.join(con.ENEMY_SPRITE_BASE, name)
                path = os.path.join(img_dir, img)
                if os.path.exists(path):
                    img_path = path

            scale = enemy_dict.get('scale', 0.6)
            shift = enemy_dict.get('height_shift', 0.38)
            anim_time = enemy_dict.get('animation_time', 180)
            speed = enemy_dict.get('speed', 0.03)
            size = enemy_dict.get('size', 20)
            attack_dist = enemy_dict.get('attack_distance', randint(3, 6))
            damage = enemy_dict.get('attack_damage', 10)
            health = enemy_dict.get('health', 100)
            accuracy = enemy_dict.get('accuracy', 0.15)
            weight = enemy_dict.get('spawn_weight', 0)

            sounds: dict[str, pg.mixer.Sound] = {}
            action_sounds = enemy_dict.get('action_sounds')
            if action_sounds:
                enemy_sounds = game.sound.get_enemy_sounds(name)
                for action in action_sounds.keys():
                    action_file = action_sounds[action]
                    if action_file in enemy_sounds:
                        sounds[action] = enemy_sounds.get(action_file)

            builder: EnemyBuilder = EnemyBuilder(game, img_path, pos) \
                .set_name(name) \
                .set_scale(scale) \
                .set_shift(shift) \
                .set_animation_time(anim_time) \
                .set_speed(speed) \
                .set_size(size) \
                .set_attack_distance(attack_dist) \
                .set_attack_damage(damage) \
                .set_health(health) \
                .set_accuracy(accuracy) \
                .set_spawn_weight(weight) \
                .set_sounds(sounds)

            return builder


def get_enemy_meta(data_dir: str, names: Optional[list[str]] = None) \
        -> tuple[dict[str, int], dict[str, str]]:
    print('Loading enemy meta data...')
    data: dict[str, int] = {}
    paths: dict[str, str] = {}
    files = os.listdir(data_dir)
    for file in files:
        ext = os.path.splitext(file)[1]
        if ext == '.json':
            full_path = os.path.join(data_dir, file)
            with open(full_path, encoding='UTF-8') as e_file:
                enemy_dict = json.load(e_file)
                name = enemy_dict.get('name')
                if names and name not in names:
                    print(f"'{name}' not specified in map data. Skipping...")
                    continue

                weight = enemy_dict.get('spawn_weight')
                if name and weight:
                    data[name] = weight
                    paths[name] = full_path

    return data, paths
