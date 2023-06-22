from collections import deque
from enum import Enum
import pygame as pg
from typing import Optional

from engine import constants as con
from engine.sprite import AnimatedSprite


class WeaponState(Enum):
    READY = 'ready'
    IDLE = 'idle'
    FIRE = 'fire'


# TODO Not sure we're going to need this
class WeaponActionType(Enum):
    PLAY_SOUND = "play_sound"
    ANIMATE = "animate"
    NONE = "none"


# TODO might not need this
class WeaponSound:

    def __init__(self, name: str, file: str):
        self.name: str = name
        self.file: str = file
        self.volume: Optional[float] = None
        self.sound: Optional[pg.mixer.Sound] = None


# TODO might not need this
class WeaponAction:

    def __init__(self):
        self.action: WeaponActionType = WeaponActionType.NONE
        self.sound: Optional[str] = None
        self.images: Optional[list[str]] = None


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
        self.name: str = ""
        self.reloading: bool = False
        self.has_continuous_fire: bool = False
        self.frame_counter: int = 0
        # TODO Damage (actual) should be = (damage x ammo_use)
        self.damage: int = 50
        self.weapon_pos = 0
        self.num_images: int = 0
        # TODO Until we have power-ups, we have no way for the player
        # to pick up more ammo. So for now, weapons essentially have
        # unlimited ammo (we don't decrement ammo count).
        self.ammo_capacity: int = 20
        self.magazine_capacity: int = 8
        self.total_ammo: int = self.ammo_capacity
        self.ammo_remaining: int = self.magazine_capacity
        self.total_ammo -= self.ammo_remaining
        self.ammo_use: int = 1
        self.sound: Optional[pg.mixer.Sound] = None
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.animation_frames: dict[str, pg.Surface] = {}
        # TODO Need variables for things like ammo capacity,
        # rate of fire, magazine capacity, etc.
        # TODO Need to support sounds for multiple events:
        # Fire, reload start, reload stop, empty, idle, hit, etc
        self._idle_prev: int = 0
        self._idle_sound_delay: int = 0
        self._has_idle_sound: bool = False

    @property
    def magazine_count(self) -> int:
        if self.ammo_remaining > 0:
            mags: int = 1
            if self.total_ammo > self.magazine_capacity > 0:
                mags += (self.total_ammo / self.magazine_capacity)
            return mags
        return 0

    def setup(self):
        if self.image:
            s_w = self.image.get_width() * self.SPRITE_SCALE
            s_h = self.image.get_height() * self.SPRITE_SCALE
            self.images = deque([
                pg.transform.smoothscale(img, (s_w, s_h))
                for img in self.images
            ])
            self.num_images = len(self.images)
            i_w = con.HALF_WIDTH - self.images[0].get_width() // 2
            i_h = con.HEIGHT - self.images[0].get_height()
            self.weapon_pos = (i_w, i_h)

        self._has_idle_sound = self.sounds.get("idle") is not None
        if self._has_idle_sound:
            self._idle_prev = pg.time.get_ticks()
            self._idle_sound_delay = 700

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
        if self._has_idle_sound and not self.reloading:
            time_now = pg.time.get_ticks()
            time_delta = time_now - self._idle_prev
            if time_delta > self._idle_sound_delay:
                self._idle_prev = time_now
                self.play_action_sound('idle')

    def play_action_sound(self, action: str):
        action_sound = self.sounds.get(action)
        if action_sound:
            action_sound.play()

    def play_attack_sound(self):
        self.play_action_sound('fire')
