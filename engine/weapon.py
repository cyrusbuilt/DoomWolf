import os.path
from collections import deque
from enum import Enum
import pygame as pg
from typing import Optional
from engine import constants as con
from engine.sprite import AnimatedSprite


class WeaponClass(Enum):
    SHOTGUN = 'shotgun'
    CHAINSAW = 'chainsaw'
    NONE = 'none'


class Weapon(AnimatedSprite):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game=game,
                         path=path,
                         scale=scale,
                         animation_time=animation_time)
        self.reloading: bool = False
        self.frame_counter: int = 0
        self.damage: int = 50
        self.weapon_pos = 0
        self.num_images: int = 0
        self.sound: Optional[pg.mixer.Sound] = None
        self.weapon_class: WeaponClass = WeaponClass.NONE
        # TODO Need an ammo count and each shot should decrement.

        if self.image:
            s_w = self.image.get_width() * scale
            s_h = self.image.get_height() * scale
            self.images = deque([
                pg.transform.smoothscale(img, (s_w, s_h))
                for img in self.images
            ])
            self.num_images = len(self.images)
            i_w = con.HALF_WIDTH - self.images[0].get_width() // 2
            i_h = con.HEIGHT - self.images[0].get_height()
            self.weapon_pos = (i_w, i_h)

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()

    def play_sound(self):
        if self.sound:
            self.sound.play()


class Shotgun(Weapon):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class = WeaponClass.SHOTGUN
        self.sound = game.sound.get_weapon_sound(self.weapon_class)


class Chainsaw(Weapon):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.5,
                 animation_time: int = 200):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class = WeaponClass.CHAINSAW
        self.sound = game.sound.get_weapon_sound(self.weapon_class)
        self.damage = 20
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
