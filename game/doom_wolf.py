import pygame as pg

from engine.game import Game
from weapon.weapon_inventory import WeaponInventory
from game.doom_obj_handler import DoomWolfObjectHandler
from game.settings import GameSettings


SETTINGS = 'settings.json'


class DoomWolf(Game):

    def __init__(self, window_title: str = 'DoomWolf'):
        super().__init__()
        self.window_title = window_title
        self.settings: GameSettings = GameSettings(SETTINGS)
        self.object_handler = DoomWolfObjectHandler(self)
        self.weapon_inventory: WeaponInventory = WeaponInventory(self)

    def new_game(self):
        super().new_game()
        self.settings.load_settings()
        self.mouse_sensitivity = self.settings.mouse_sensitivity
        self.current_weapon = self.weapon_inventory.get_current()
        self.sound.set_music_volume(self.settings.music_volume)
        if self.settings.launch_fullscreen and not pg.display.is_fullscreen():
            pg.display.toggle_fullscreen()

    def do_event(self, event: pg.event.Event):
        self.weapon_inventory.inventory_event(event)
