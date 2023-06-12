from collections import deque
import pygame as pg
from typing import Optional

from engine import constants as con
from engine.sprite import AnimatedSprite


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
        self.has_continuous_fire: bool = False
        self.frame_counter: int = 0
        self.damage: int = 50
        self.weapon_pos = 0
        self.num_images: int = 0
        self.sound: Optional[pg.mixer.Sound] = None
        # TODO Need variables for things like ammo capacity,
        # rate of fire, magazine capacity, etc.
        # TODO Need to support sounds for multiple events:
        # Fire, reload start, reload stop, empty, idle, hit, etc

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
