import os
from typing import Optional

from engine import constants as con
from engine.enemy import Enemy
from engine.object_handler import ObjectHandler
from engine.sprite import AnimatedSprite
from engine.sprite import Sprite
from enemy import get_enemy_meta
from enemy import enemy
from maps.sprite_map import SpriteMap


class DoomWolfObjectHandler(ObjectHandler):

    def __init__(self, game):
        super().__init__(game)
        self.enemy_paths: dict[str, str] = {}
        self.sprite_map: Optional[SpriteMap] = None

    def setup(self):
        super().setup()
        data, paths = get_enemy_meta(con.ENEMY_DATA_BASE)
        items = data.items()
        spawn_weights = dict(sorted(items, key=lambda item: item[1], reverse=True))
        self.enemy_types = list(spawn_weights.keys())
        self.weights = list(spawn_weights.values())
        self.enemy_paths = paths

    def build_enemy_npc(self, game, klass: str, pos: tuple[float, float]) -> Enemy:
        path = self.enemy_paths[klass]
        return enemy(game, path, pos).build()

    def spawn_sprites(self):
        if self.sprite_map:
            self.sprite_list = []
            for a_sprite in self.sprite_map.animated_sprites:
                s_path = os.path.join(con.ANIM_SPRITE_BASE, a_sprite.name)
                s_path = os.path.join(s_path, "0.png")
                if not a_sprite.pos_x and not a_sprite.pos_y:
                    self.add_sprite(AnimatedSprite(self.game, s_path))
                else:
                    pos = (a_sprite.pos_x, a_sprite.pos_y)
                    self.add_sprite(AnimatedSprite(self.game, s_path, pos))

            for s_sprite in self.sprite_map.static_sprites:
                s_path = os.path.join(con.STATIC_SPRITE_BASE, s_sprite.name)
                s_path = os.path.join(s_path, "0.png")
                if not s_sprite.pos_x and not s_sprite.pos_y:
                    self.add_sprite(Sprite(self.game, s_path))
                else:
                    pos = (s_sprite.pos_x, s_sprite.pos_y)
                    self.add_sprite(Sprite(self.game, s_path, pos))

            for d_sprite in self.sprite_map.door_sprites:
                self.add_sprite(d_sprite)
                for i in range(d_sprite.tile_count):
                    pos = (int(d_sprite.x - i), int(d_sprite.y))
                    self.game.map.add_obstacle(pos)
        else:
            super().spawn_sprites()
