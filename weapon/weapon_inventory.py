import os
import pygame as pg

from engine import constants as con
from engine.weapon import Weapon
from weapon import weapon


class WeaponInventory:

    def __init__(self, game):
        self.game = game
        self.inv_weapons: dict[str, Weapon] = {}
        self.current_weapon: str = ''

    def get_current(self) -> Weapon:
        return self.inv_weapons[self.current_weapon]

    def load_weapons(self):
        self.inv_weapons = {}
        for file in os.listdir(con.WEAPON_DATA_BASE):
            ext = os.path.splitext(file)[1]
            if ext == '.json':
                full_path = os.path.join(con.WEAPON_DATA_BASE, file)
                wpn = weapon(self.game, full_path).build()
                self.inv_weapons[wpn.name] = wpn

        if self.inv_weapons:
            self.current_weapon = next(iter(self.inv_weapons))

    def get_next_weapon_index(self) -> int:
        weapon_names = list(self.inv_weapons.keys())
        current_index = weapon_names.index(self.current_weapon)
        next_index = current_index
        if current_index < len(weapon_names) - 1:
            next_index += 1
        elif current_index + 1 >= len(weapon_names):
            next_index = 0

        if next_index != current_index:
            return next_index

        return -1

    def next(self):
        next_index = self.get_next_weapon_index()
        if next_index > -1:
            weapon_names = list(self.inv_weapons.keys())
            self.current_weapon = weapon_names[next_index]
            print(f'Switching weapon to: {self.current_weapon}')
            self.game.current_weapon = self.get_current()

    def inventory_event(self, event: pg.event.Event):
        tab_pressed = event.type == pg.KEYDOWN and \
            event.key == pg.K_TAB
        b_pressed = event.type == pg.JOYBUTTONDOWN and \
            event.button == 1

        if tab_pressed or b_pressed:
            self.next()

    def drop_current(self):
        next_index = self.get_next_weapon_index()
        if next_index == -1:
            # Can't switch weapons since this is the only weapon we have.
            return

        current_name = self.current_weapon
        self.next()
        self.inv_weapons.pop(current_name)

    def pickup(self, wpn: Weapon):
        if self.inv_weapons.get(wpn.name) is not None:
            self.inv_weapons[wpn.name] = wpn
            self.current_weapon = wpn.name
            self.game.current_weapon = self.get_current()
