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
        self.name: str = ""
        self.reloading: bool = False
        self.has_continuous_fire: bool = False
        self.frame_counter: int = 0
        # TODO Damage (actual) should be = (damage x ammo_use)
        self.damage: int = 50
        self.weapon_pos = 0
        self.num_images: int = 0
        self.ammo_capacity: int = 32
        self.magazine_capacity: int = 8
        self.total_ammo: int = self.ammo_capacity
        self.ammo_remaining: int = self.magazine_capacity
        self.magazine_count: int = int(self.total_ammo / self.magazine_capacity) - 1
        self.ammo_use: int = 1
        self.sound: Optional[pg.mixer.Sound] = None
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.animation_frames: dict[str, pg.Surface] = {}
        self._idle_prev: int = 0
        self._idle_sound_delay: int = 0
        self._has_idle_sound: bool = False
        self._mag_change_trigger: bool = False
        self.reload_anim_frames: dict[str, pg.Surface] = {}
        self.reload_anim_images: deque[pg.Surface] = deque()
        self.spindown_anim_frames: dict[str, pg.Surface] = {}
        self.spindown_anim_images: deque[pg.Surface] = deque()
        self._mag_change_complete: bool = True
        self._fire_complete: bool = True
        self._spindown_complete: bool = True
        self._spindown_trigger: bool = False
        self._original_images: deque[pg.Surface] = deque()
        self.custom_reload_sounds: Optional[dict[int, str]] = None
        self.custom_fire_sounds: Optional[dict[int, str]] = None

    def setup(self):
        self.total_ammo = self.ammo_capacity
        self.ammo_remaining = self.magazine_capacity
        self.magazine_count = int(self.total_ammo / self.magazine_capacity) - 1
        if self.ammo_capacity == -1:
            self.ammo_remaining = -1

        if self.image:
            s_w = self.image.get_width() * self.SPRITE_SCALE
            s_h = self.image.get_height() * self.SPRITE_SCALE
            self.images = deque([
                pg.transform.smoothscale(img, (s_w, s_h))
                for img in self.images
            ])

            self._original_images = self.images
            self.num_images = len(self.images)

            i_w = con.HALF_WIDTH - self.images[0].get_width() // 2
            i_h = con.HEIGHT - self.images[0].get_height()
            self.weapon_pos = (i_w, i_h)

            if len(self.reload_anim_images):
                self.reload_anim_images = deque([
                    pg.transform.smoothscale(img, (s_w, s_h))
                    for img in self.reload_anim_images
                ])

            if len(self.spindown_anim_images):
                self.spindown_anim_images = deque([
                    pg.transform.smoothscale(img, (s_w, s_h))
                    for img in self.spindown_anim_images
                ])

        self._has_idle_sound = self.sounds.get("idle") is not None
        if self._has_idle_sound:
            self._idle_prev = pg.time.get_ticks()
            self._idle_sound_delay = 700

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.ammo_remaining == 0 and self._fire_complete:
                self.reloading = False
                return

            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                if (self.custom_fire_sounds and
                        self.frame_counter in self.custom_fire_sounds):
                    sound_action = self.custom_fire_sounds[self.frame_counter]
                    self.play_action_sound(sound_action)

                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self._fire_complete = True
                    self.frame_counter = 0
                    self.reloading = False
                    self._spindown_trigger = True

    def animate_reload(self):
        if len(self.reload_anim_images) > 0:
            self._mag_change_complete = False
            if self.animation_trigger:
                self.reload_anim_images.rotate(-1)
                self.image = self.reload_anim_images[0]
                if (self.custom_reload_sounds and
                        self.frame_counter in self.custom_reload_sounds):
                    sound_action = self.custom_reload_sounds[self.frame_counter]
                    self.play_action_sound(sound_action)

                self.frame_counter += 1
                if self.frame_counter == len(self.reload_anim_images):
                    self.frame_counter = 0
                    self._mag_change_complete = True

    def animate_spindown(self):
        if len(self.spindown_anim_images) > 0:
            self._spindown_complete = False
            if self.animation_trigger:
                self.spindown_anim_images.rotate(-1)
                self.image = self.spindown_anim_images[0]
                self.frame_counter += 1
                if self.frame_counter == len(self.spindown_anim_images):
                    self.frame_counter = 0
                    self._spindown_complete = True

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        if self._mag_change_trigger:
            self.animate_reload()
        else:
            self.animate_shot()

        if self._spindown_trigger and not self.game.player.shot:
            self.animate_spindown()

        if self._spindown_trigger and self._spindown_complete:
            self._spindown_trigger = False
            self.images = self._original_images

        if self._has_idle_sound and not self.reloading:
            time_now = pg.time.get_ticks()
            time_delta = time_now - self._idle_prev
            if time_delta > self._idle_sound_delay:
                self._idle_prev = time_now
                self.play_action_sound('idle')

        if self._mag_change_trigger and self._mag_change_complete:
            self.play_action_sound('mag_in')
            self._mag_change_trigger = False
            self.images = self._original_images

            # Mag change complete. Recompute ammo.
            if self.magazine_count > 0:
                self.ammo_remaining = self.magazine_capacity
                self.total_ammo -= self.ammo_remaining
                self.magazine_count -= 1
            else:
                self.ammo_remaining = 0
                self.total_ammo = 0

    def play_action_sound(self, action: str):
        action_sound = self.sounds.get(action)
        if action_sound:
            self.game.sound.play_sound(action_sound)
        else:
            print(f"Sound not found for weapon action: '{action}'")

    def fire(self):
        if self.ammo_remaining == -1 and self.ammo_capacity == -1:
            self.play_action_sound('fire')
            return

        if self.ammo_remaining > 0:
            self._fire_complete = False
            self.play_action_sound('fire')
            self.ammo_remaining -= self.ammo_use

        if self.ammo_remaining <= 0 < self.total_ammo and self._fire_complete:
            self._mag_change_trigger = True
            self.images = self.reload_anim_images
            self.play_action_sound('mag_out')

        if self.ammo_remaining <= 0 and self.total_ammo == 0:
            self.play_action_sound('empty')

    def give_ammo(self, ammo: int) -> bool:
        if (self.ammo_remaining == self.magazine_capacity and
                self.total_ammo == self.ammo_capacity):
            return False

        print(f'Player took ammo: {ammo}')
        if ammo > self.ammo_capacity:
            ammo = self.ammo_capacity

        if ammo < 1:
            ammo = 1

        if (self.total_ammo + ammo) > self.ammo_capacity:
            self.total_ammo = self.ammo_capacity
            self.ammo_remaining = self.magazine_capacity
        else:
            if (self.ammo_remaining + ammo) > self.magazine_capacity:
                diff = ammo - self.ammo_remaining
                self.ammo_remaining = self.magazine_capacity
                if (self.total_ammo + diff) > self.ammo_capacity:
                    self.total_ammo = self.ammo_capacity
            else:
                self.ammo_remaining += ammo

        self.magazine_count = int(self.total_ammo / self.magazine_capacity) - 1
        self._mag_change_trigger = True
        self.images = self.reload_anim_images
        self.play_action_sound('mag_out')
        return True
