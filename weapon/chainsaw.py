import os
import pygame as pg
from typing import Optional

from weapon import WeaponBase
from weapon import WeaponClass


class Chainsaw(WeaponBase):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.5,
                 animation_time: int = 200):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class = WeaponClass.CHAINSAW
        self.sound = game.sound.get_weapon_sound(self.weapon_class)
        self.damage = 30
        self.time_prev: int = 0
        self.idle_sound_delay: int = 0

        # Chainsaw is a bit of a special case. It has an 'idle' sound
        # that needs to play in a loop when not firing.
        self.idle_sound: Optional[pg.mixer.Sound] = None
        weapon_path = os.path.join(game.sound.path, 'weapon')
        idle_path = os.path.join(weapon_path, 'chainsaw_idle.wav')
        if os.path.exists(idle_path):
            print(f'Loading idle weapon sound: {idle_path}')
            self.idle_sound = pg.mixer.Sound(idle_path)
            self.time_prev = pg.time.get_ticks()
            self.idle_sound_delay = 700

    def update(self):
        super().update()
        if self.idle_sound and not self.reloading:
            time_now = pg.time.get_ticks()
            time_delta = time_now - self.time_prev
            if time_delta > self.idle_sound_delay:
                self.time_prev = time_now
                self.idle_sound.play()
