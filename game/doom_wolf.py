import json
import os
import pygame as pg
from typing import Optional

from engine import constants as con
from engine import Resolution
from engine.game import Game
from engine.input_handler import InputEvent
from game.doom_obj_handler import DoomWolfObjectHandler
from game.settings import GameSettings
from maps import game_map
from maps.sprite_map import sprite_map
from screens.load_game import LoadGameMenu
from screens.pause_screen import PauseScreen
from weapon.weapon_inventory import WeaponInventory


SETTINGS = 'settings.json'


class DoomWolf(Game):

    def __init__(self, window_title: str = 'DoomWolf',
                 settings: Optional[GameSettings] = None):
        super().__init__()
        self.window_title = window_title
        if settings is None:
            settings = GameSettings(SETTINGS)

        self.settings: GameSettings = settings
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
            self.screen = pg.display.set_mode(res, pg.HWSURFACE)

        if self.settings.launch_fullscreen and not pg.display.is_fullscreen():
            pg.display.toggle_fullscreen()

    def _add_pause_screen(self):
        self.pause_screen = PauseScreen(self)
        lg_menu = LoadGameMenu(self.pause_screen.get_current())
        lg_menu.setup()
        self.pause_screen.set_load_game_menu(lg_menu)

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
        else:
            [e.setup() for e in self.object_handler.enemy_list]

        s_map = self.map.sprite_map_path
        if s_map and os.path.exists(s_map):
            sprites = sprite_map(self, s_map).build()
            self.object_handler.sprite_map = sprites

        super().new_game(have_maps)
        self.settings.load_settings()
        self._apply_settings()

        self.weapon_inventory.load_weapons()
        self.current_weapon = self.weapon_inventory.get_current()

        self._add_pause_screen()

    def _find_map_by_name(self, name: str) -> Optional[str]:
        result = None
        for the_map in self.maps:
            with open(the_map, encoding='UTF-8') as file:
                data = json.load(file)
                if data['name'] == name:
                    result = the_map
                    break
        return result

    def load_game(self, save_game_data: dict):
        map_name = save_game_data.get('map')
        player_data = save_game_data.get('player')
        weapon_data = save_game_data.get('weapon')
        door_data = save_game_data.get('doors')
        enemy_data = save_game_data.get('enemies')
        item_data = save_game_data.get('items')

        the_map = self._find_map_by_name(map_name)
        if not the_map:
            # TODO fallback to new_game() instead?
            return

        self.map = game_map(self, the_map).build()
        if self.map.enemies:
            self.object_handler.enemy_names = self.map.enemies

        s_map = self.map.sprite_map_path
        if s_map and os.path.exists(s_map):
            sprites = sprite_map(self, s_map).build()
            if door_data:
                for d in sprites.door_sprites:
                    for d_data in door_data:
                        if d.id == d_data['id']:
                            d.x = d_data['pos_x']
                            d.y = d_data['pos_y']
                            d.is_interactive = d_data['interactive']
                            d.removed = d_data['removed']
                            d.tile_count = d_data['tile_count']
                            d.previous_pos_x = d_data['previous_pos_x']
                            d.previous_pos_y = d_data['previous_pos_y']
                            for i in range(d.tile_count):
                                my_x = int(d.previous_pos_x - i)
                                my_y = int(d.previous_pos_y)
                                my_pos = (my_x, my_y)
                                if self.map.has_obstacle(my_pos):
                                    self.map.remove_obstacle(my_pos)

            if item_data:
                for i in sprites.item_sprites:
                    for i_data in item_data:
                        if i.id == i_data['id']:
                            i.is_interactive = i_data['interactive']
                            i.x = i_data['pos_x']
                            i.y = i_data['pos_y']
                            i.removed = i_data['removed']

            self.object_handler.sprite_map = sprites

        super().new_game(True)
        self.settings.load_settings()
        self._apply_settings()

        if enemy_data:
            # Override the auto-generated enemies
            self.object_handler.enemy_list = []
            for e in enemy_data:
                pos = (e['pos_x'], e['pos_y'])
                enemy = self.object_handler.build_enemy_npc(self, e['name'],
                                                            pos)
                enemy.x = e['pos_x']
                enemy.y = e['pos_y']
                enemy.alive = e['alive']
                enemy.health = e['health']
                enemy.removed = e['removed']
                enemy.player_search_trigger = e['player_search_trigger']
                enemy.ray_cast_value = e['ray_cast_value']
                self.object_handler.add_enemy(enemy)

        if player_data:
            self.player.x = player_data['pos_x']
            self.player.y = player_data['pos_y']
            self.player.health = player_data['health']
            self.player.armor = player_data['armor']
            self.player.angle = player_data['angle']
            self.player.rel = player_data['rel']

        self.weapon_inventory.load_weapons()
        if weapon_data:
            self.weapon_inventory.current_weapon = weapon_data['current']
            curr_weapon = self.weapon_inventory.get_current()
            curr_weapon.total_ammo = weapon_data['total_ammo']
            curr_weapon.ammo_remaining = weapon_data['remaining_ammo']
            self.current_weapon = curr_weapon

        self._add_pause_screen()
        print('Save game loaded. Resuming game...')

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
            lm = self.pause_screen.load_game_menu
            save_data = lm.get_selected_save_game_data()
            if save_data:
                self.pause_screen.close_menu()
                self.load_game(save_data)

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

    def load_test_map(self, map_path: str):
        if os.path.exists(map_path):
            print(f'Loading test map: {map_path}')
            self.maps.clear()
            self.maps.append(map_path)
            self.test_mode = True
