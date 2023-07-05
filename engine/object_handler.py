from random import choices, randrange
import pygame as pg
from typing import Optional

from engine import constants as con
from engine.common import align_grid
from engine.enemy import Enemy
from engine.sprite import AnimatedSprite
from engine.sprite import Sprite


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.sprite_list: list[Sprite] = []
        self.enemy_list: list[Enemy] = []
        self.enemy_sprite_path: str = con.ENEMY_SPRITE_BASE
        self.static_sprite_path: str = con.STATIC_SPRITE_BASE
        self.anim_sprite_path: str = con.ANIM_SPRITE_BASE
        self.enemy_positions: dict[tuple[int, int]] = {}
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.enemy_count: int = 20
        self.enemy_types: list[str] = []
        self.weights: list[int] = []

    def setup(self):
        pass

    def build_enemy_npc(self, game, klass: str, pos: tuple[float, float]) -> Enemy:
        return Enemy(self.game, '')

    def spawn_enemies(self):
        self.enemy_list = []
        for _ in range(self.enemy_count):
            x = randrange(self.game.map.cols)
            y = randrange(self.game.map.rows)
            pos = x, y
            pos_in_map = pos in self.game.map.world_map
            pos_in_res_area = pos in self.restricted_area
            while pos_in_map or pos_in_res_area:
                x = randrange(self.game.map.cols)
                y = randrange(self.game.map.rows)
                pos = x, y
                pos_in_map = pos in self.game.map.world_map
                pos_in_res_area = pos in self.restricted_area

            npc_type = choices(self.enemy_types, self.weights)[0]
            enemy = self.build_enemy_npc(self.game, npc_type, (x + 0.5, y + 0.5))
            self.add_enemy(enemy)

    def spawn_sprites(self):
        self.sprite_list = []
        green_light = f'{self.anim_sprite_path}/green_light/0.png'
        red_light = f'{self.anim_sprite_path}/red_light/0.png'
        self.add_sprite(AnimatedSprite(self.game, green_light))
        self.add_sprite(AnimatedSprite(self.game, green_light, (1.5, 1.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (1.5, 7.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (5.5, 3.25)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (5.5, 4.75)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (7.5, 2.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (7.5, 5.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (14.5, 1.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (14.5, 4.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (14.5, 5.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (14.5, 7.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (12.5, 7.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (9.5, 7.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (14.5, 12.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (9.5, 20.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (10.5, 20.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (3.5, 14.5)))
        self.add_sprite(AnimatedSprite(self.game, red_light, (3.5, 18.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (14.5, 24.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (14.5, 30.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (1.5, 30.5)))
        self.add_sprite(AnimatedSprite(self.game, green_light, (1.5, 24.5)))

    def spawn_entities(self):
        self.spawn_sprites()
        self.spawn_enemies()

    def check_win(self):
        if not len(self.enemy_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.map.won = True
            self.game.new_game()

    def update(self):
        self.enemy_positions = {
            npc.map_pos
            for npc in self.enemy_list if npc.alive
        }

        if self.game.player.interact:
            for sprite in sorted(self.sprite_list, key=lambda obj: obj.norm_dist):
                player = self.game.player
                px, py = align_grid(player.x, player.y)
                sx, sy = align_grid(sprite.x, sprite.y)
                x_dist = px - sx
                y_dist = py - sy
                if sprite.is_interactive:
                    if ((-con.INTERACTION_RANGE <= x_dist <= con.INTERACTION_RANGE) and (
                            -con.INTERACTION_RANGE <= y_dist <= con.INTERACTION_RANGE)) and not sprite.interact_trigger:
                        sprite.interact_trigger = True

        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.enemy_list]
        self.check_win()

    def add_enemy(self, enemy: Optional[Enemy]):
        if enemy:
            self.enemy_list.append(enemy)

    def add_sprite(self, sprite: Optional[Sprite]):
        if sprite:
            self.sprite_list.append(sprite)
