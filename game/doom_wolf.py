import pygame as pg

from engine.game import Game
from weapon.weapon_inventory import WeaponInventory
from game.doom_obj_handler import DoomWolfObjectHandler


class DoomWolf(Game):

    def __init__(self, window_title: str = 'DoomWolf'):
        super().__init__()
        self.window_title = window_title
        self.object_handler = DoomWolfObjectHandler(self)
        self.weapon_inventory: WeaponInventory = WeaponInventory(self)

    def new_game(self):
        super().new_game()
        self.current_weapon = self.weapon_inventory.get_current()

    def do_event(self, event: pg.event.Event):
        self.weapon_inventory.inventory_event(event)
