from enum import Enum
import pygame as pg

from engine import constants as con
from engine.sprite import AnimatedSprite


class ItemType(Enum):
    AMMO = 'ammo'
    ARMOR = 'armor'
    HEALTH = 'health'
    GENERIC = 'generic'


class Item(AnimatedSprite):

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (11.5, 3.5),
                 scale: float = 0.8,
                 shift: float = 0.16,
                 animation_time: int = 120):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name: str = ""
        self.type: ItemType = ItemType.GENERIC
        w = int(con.GRID_BLOCK - 36)
        h = int(con.GRID_BLOCK - 36)
        self.rect = pg.Rect(pos[0], pos[1], w, h)
        self.rect.center = (pos[0] + w / 2, pos[1] + h / 2)
        self.units: int = 0
        self.is_interactive = True

    @property
    def id(self) -> str:
        return f'{self.name}_{int(self.x)}_{int(self.y)}'

    def update(self):
        self.refresh_sprite()
        self.check_animation_time()
        self.animate(self.images)

        picked_up = False
        if self.rect:
            if self.rect.colliderect(self.game.player.rect):
                if self.type == ItemType.HEALTH:
                    picked_up = self.game.player.give_health(self.units)
                elif self.type == ItemType.ARMOR:
                    picked_up = self.game.player.give_armor(self.units)
                # TODO Handle other types

                if picked_up:
                    super().interact()
                    self.removed = True

                sprite_list = self.game.object_handler.sprite_list
                if self in sprite_list and self.removed:
                    sprite_list.remove(self)
                    self.rect = None
