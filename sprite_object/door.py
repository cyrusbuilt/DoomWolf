import pygame as pg
from enum import Enum

from engine import constants as con
from engine.sprite import AnimatedSprite


class DoorType(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class Door(AnimatedSprite):

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (11.5, 3.5),
                 scale: float = 0.8,
                 shift: float = 0.16,
                 animation_time: int = 120):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.SCALE_WIDTH: float = 1.0
        self.tile_count: int = 1
        self.is_interactive = True
        self.type: DoorType = DoorType.HORIZONTAL
        self.previous_pos_x: float = self.x
        self.previous_pos_y: float = self.y
        self.id: int = hash(self)

    def interact(self):
        if self.removed:
            return

        # We want the interaction sound to only play once.
        super().interact()
        self.is_interactive = False

        if self.type == DoorType.VERTICAL:
            self.y -= 1
            delta_y = self.y - self.previous_pos_y
            if abs(delta_y) > con.FIFTH_BLOCK:
                self.removed = True
        elif self.type == DoorType.HORIZONTAL:
            self.x -= 1
            delta_x = self.x - self.previous_pos_x
            if abs(delta_x) > con.FIFTH_BLOCK:
                self.removed = True

        if self.removed:
            for i in range(self.tile_count):
                my_x = int(self.previous_pos_x - i)
                my_y = int(self.previous_pos_y)
                my_pos = (my_x, my_y)
                if self.game.map.has_obstacle(my_pos):
                    self.game.map.remove_obstacle(my_pos)

    def get_sprite_projection(self):
        if not self.image:
            return

        proj_height = con.SCREEN_DIST / self.norm_dist
        sprite_width = proj_height * self.SCALE_WIDTH
        sprite_height = proj_height * self.SPRITE_SCALE

        image = pg.transform.scale(self.image, (sprite_width, sprite_height))

        self.sprite_half_width = sprite_width // 2
        height_shift = sprite_height * self.SPRITE_HEIGHT_SHIFT
        w = self.screen_x - self.sprite_half_width
        h = con.HALF_HEIGHT - sprite_height // 2 + height_shift
        pos = w, h

        self.game.ray_caster.objects_to_render.append(
            (self.norm_dist, image, pos))

    def update(self):
        if self.removed:
            return

        self.check_animation_time()
        self.refresh_sprite()
        if self.interact_trigger and self.animation_trigger:
            self.animate(self.images)
            self.interact()
