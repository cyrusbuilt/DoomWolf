import os
import pygame as pg

from engine import constants as con
from engine.game import Game
from weapon.weapon_inventory import WeaponInventory
from game.doom_obj_handler import DoomWolfObjectHandler
from game.settings import GameSettings
from maps import game_map
from maps.sprite_map import sprite_map


SETTINGS = 'settings.json'


class DoomWolf(Game):

    def __init__(self, window_title: str = 'DoomWolf'):
        super().__init__()
        self.window_title = window_title
        self.settings: GameSettings = GameSettings(SETTINGS)
        self.object_handler = DoomWolfObjectHandler(self)
        self.weapon_inventory: WeaponInventory = WeaponInventory(self)
        self.maps: list[str] = []
        self.current_map_index: int = -1

    def new_game(self):
        have_maps = False
        if self.map is None or self.map.won:
            have_maps = len(self.maps) > 0
            if have_maps:
                if (self.current_map_index + 1) < len(self.maps):
                    self.current_map_index += 1
                path = self.maps[self.current_map_index]
                self.map = game_map(self, path).build()

                s_map = self.map.sprite_map_path
                if s_map and os.path.exists(s_map):
                    sprites = sprite_map(self, s_map).build()
                    self.object_handler.sprite_map = sprites

        super().new_game(have_maps)
        self.settings.load_settings()
        self.weapon_inventory.load_weapons()
        self.mouse_sensitivity = self.settings.mouse_sensitivity
        self.current_weapon = self.weapon_inventory.get_current()
        self.sound.set_music_volume(self.settings.music_volume)
        if self.settings.launch_fullscreen and not pg.display.is_fullscreen():
            pg.display.toggle_fullscreen()

    def do_event(self, event: pg.event.Event):
        self.weapon_inventory.inventory_event(event)

    def find_maps(self):
        items = os.listdir(con.MAP_DATA_BASE)
        items = [d for d in items
                 if os.path.isdir(os.path.join(con.MAP_DATA_BASE, d))]
        items = sorted(items)
        for map_dir in items:
            dir_path = os.path.join(con.MAP_DATA_BASE, map_dir)
            map_file = os.path.join(dir_path, f'{map_dir}.json')
            if os.path.exists(map_file):
                print(f'Found map file: {map_file}')
                self.maps.append(map_file)
