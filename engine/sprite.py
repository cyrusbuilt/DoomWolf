import math
from collections import deque
import os
import pygame as pg
from typing import Optional
from engine import constants as con
from engine.player import Player


class Sprite:

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (10.5, 3.5),
                 scale: float = 0.7,
                 shift: float = 0.27):
        self.game = game
        self.player: Player = game.player
        self.x: float = pos[0]
        self.y: float = pos[1]
        self.image: Optional[pg.Surface] = None
        self.dx = 0
        self.dy = 0
        self.theta = 0
        self.screen_x = 0
        self.dist = 1
        self.norm_dist = 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.IMAGE_WIDTH = 0
        self.IMAGE_HALF_WIDTH = 0
        self.IMAGE_RATIO = 0

        if os.path.exists(path):
            self.image = pg.image.load(path).convert_alpha()
            self.IMAGE_WIDTH = self.image.get_width()
            self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
            self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()

    def get_sprite_projection(self):
        proj = con.SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width = proj * self.IMAGE_RATIO
        proj_height = proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        w = self.screen_x - self.sprite_half_width
        h = con.HALF_HEIGHT - proj_height // 2 + height_shift
        pos = w, h

        self.game.ray_caster.objects_to_render.append(
            (self.norm_dist, image, pos))

    def refresh_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx = dx
        self.dy = dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / con.DELTA_ANGLE
        self.screen_x = (con.HALF_NUM_RAYS + delta_rays) * con.SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        total_width = con.WIDTH + self.IMAGE_HALF_WIDTH
        acceptable_width = -self.IMAGE_HALF_WIDTH < self.screen_x < total_width
        if acceptable_width and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.refresh_sprite()


class AnimatedSprite(Sprite):

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (11.5, 3.5),
                 scale: float = 0.8,
                 shift: float = 0.16,
                 animation_time: int = 120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time: int = animation_time
        self.path: str = ''
        self.images: deque[pg.Surface] = deque()
        self.animation_time_prev: int = pg.time.get_ticks()
        self.animation_trigger: bool = False

        if os.path.exists(path):
            self.path = path.rsplit('/', 1)[0]
            self.images = self.load_images(self.path)

    @staticmethod
    def load_images(path: str) -> deque[pg.Surface]:
        print(f'Loading images for sprite: {os.path.dirname(path)}')
        images: deque[pg.Surface] = deque()
        if os.path.exists(path):
            files = sorted(os.listdir(path))
            for file_name in files:
                if os.path.splitext(file_name)[1] != '.png':
                    continue

                full_path = os.path.join(path, file_name)
                if os.path.isfile(full_path):
                    img = pg.image.load(full_path).convert_alpha()
                    images.append(img)
        return images

    def animate(self, images: deque[pg.Surface]):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        time_delta = time_now - self.animation_time_prev
        if time_delta > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
