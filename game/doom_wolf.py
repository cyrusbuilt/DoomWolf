import os
import pygame as pg
from typing import Optional

from engine import constants as con
from engine import Resolution
from engine.game import Game
from engine.input_handler import InputEvent
from weapon.weapon_inventory import WeaponInventory
from game.doom_obj_handler import DoomWolfObjectHandler
from game.settings import GameSettings
from maps import game_map
from maps.sprite_map import sprite_map
from screens.pause_screen import PauseScreen


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
        self.pause_screen: Optional[PauseScreen] = None

    def _apply_settings(self):
        self.input.mouse_sensitivity = self.settings.mouse_sensitivity
        self.input.mouse_fire_button = self.settings.mouse_fire_button
        self.input.joy_fire_button = self.settings.joy_fire_button
        self.input.joy_pause_button = self.settings.joy_pause_button
        self.input.joy_quit_button = self.settings.joy_quit_button
        self.input.joy_use_button = self.settings.joy_use_button
        self.input.joy_weapon_switch = self.settings.joy_weapon_switch
        self.input.joy_left_bumper = self.settings.joy_left_bumper
        self.input.joy_right_bumper = self.settings.joy_right_bumper
        self.input.joy_d_pad_x_axis = self.settings.joy_d_pad_x_axis
        self.input.joy_d_pad_y_axis = self.settings.joy_d_pad_y_axis

        self.sound.set_music_volume(self.settings.music_volume)
        if self.settings.resolution != Resolution.zero():
            res = self.settings.resolution.to_tuple()
            self.screen = pg.display.set_mode(res)

        if self.settings.launch_fullscreen and not pg.display.is_fullscreen():
            pg.display.toggle_fullscreen()

    def new_game(self):
        have_maps = False
        if self.map is None or self.map.won:
            have_maps = len(self.maps) > 0
            if have_maps:
                if (self.current_map_index + 1) < len(self.maps):
                    self.current_map_index += 1
                path = self.maps[self.current_map_index]
                self.map = game_map(self, path).build()
                if self.map.enemies:
                    self.object_handler.enemy_names = self.map.enemies

                s_map = self.map.sprite_map_path
                if s_map and os.path.exists(s_map):
                    sprites = sprite_map(self, s_map).build()
                    self.object_handler.sprite_map = sprites

        super().new_game(have_maps)
        self.settings.load_settings()
        self._apply_settings()

        self.weapon_inventory.load_weapons()
        self.current_weapon = self.weapon_inventory.get_current()

        self.pause_screen = PauseScreen(self)

    def handle_pause(self):
        super().handle_pause()
        if (self.paused and self.pause_screen and
                not self.pause_screen.is_shown):
            self.pause_screen.show_menu()

    def do_events(self, events: set[InputEvent]):
        self.weapon_inventory.inventory_event(events)
        if (self.paused and self.pause_screen and
                self.pause_screen.is_shown):
            self.pause_screen.event_loop()

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
