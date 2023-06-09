import os
import pygame as pg

from engine.weapon import Chainsaw
from engine.weapon import Shotgun
from engine.weapon import Weapon
from engine.weapon import WeaponClass


class WeaponInventory:

    def __init__(self, game):
        self.game = game
        self.inventory: list[WeaponClass] = [
            k for k in WeaponClass if k != WeaponClass.NONE
        ]
        self.current: WeaponClass = WeaponClass.SHOTGUN
        self.path: str = 'assets/sprites/weapon'
        self.shotgun_path: str = os.path.join(self.path,
                                              WeaponClass.SHOTGUN.value,
                                              '0.png')

    def get_current(self) -> Weapon:
        img_path = os.path.join(self.path, self.current.value, '0.png')
        if self.current == WeaponClass.SHOTGUN:
            return Shotgun(self.game, img_path)
        if self.current == WeaponClass.CHAINSAW:
            return Chainsaw(self.game, img_path)

    def get_next_weapon_index(self) -> int:
        current_index = self.inventory.index(self.current)
        next_index = current_index
        if current_index < len(self.inventory) - 1:
            next_index += 1
        elif current_index + 1 >= len(self.inventory):
            next_index = 0

        if next_index != current_index:
            return next_index

        return -1

    def next(self):
        next_index = self.get_next_weapon_index()
        if next_index > -1:
            self.current = self.inventory[next_index]
            print(f'Switching weapon to: {self.current.value}')
            self.game.current_weapon = self.get_current()

    def inventory_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                self.next()

    def drop_current(self):
        next_index = self.get_next_weapon_index()
        if next_index == -1:
            # Can't switch weapons since this is the only weapon we have.
            return

        current_index = self.inventory.index(self.current)
        self.next()
        self.inventory.pop(current_index)

    def pickup(self, weapon: WeaponClass):
        exists = True
        try:
            self.inventory.index(weapon)
        except ValueError:
            exists = False

        if not exists:
            self.inventory.append(weapon)
            self.current = weapon
            self.game.current_weapon = self.get_current()
