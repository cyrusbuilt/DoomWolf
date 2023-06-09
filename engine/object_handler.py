from random import choices, randrange
import pygame as pg
from typing import Optional

from engine.enemy import Enemy
from engine.sprite import AnimatedSprite
from engine.sprite import Sprite
from enemy import EnemyClass


class ObjectHandler:

    def __init__(self, game):
        self.game = game
        self.sprite_list: list[Sprite] = []
        self.enemy_list: list[Enemy] = []
        self.enemy_sprite_path: str = 'assets/sprites/enemy'
        self.static_sprite_path: str = 'assets/sprites/static'
        self.anim_sprite_path: str = 'assets/sprites/animated_sprites'
        self.enemy_positions: dict[tuple[int, int]] = {}
        self.enemy_count: int = 20
        self.enemy_types: list[EnemyClass] = [
            EnemyClass.SOLDIER, EnemyClass.CACO_DEMON, EnemyClass.CYBER_DEMON
        ]
        self.weights: list[int] = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}

    def build_enemy_npc(self, game, klass: EnemyClass, pos: tuple[float, float]) -> Enemy:
        return Enemy(self.game, '')

    def spawn_enemies(self):
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

        # x = randrange(self.game.map.cols)
        # y = randrange(self.game.map.rows)
        # pos = x, y
        # pos_in_map = pos in self.game.map.world_map
        # pos_in_res_area = pos in self.restricted_area
        # while pos_in_map or pos_in_res_area:
        #     x = randrange(self.game.map.cols)
        #     y = randrange(self.game.map.rows)
        #     pos = x, y
        #     pos_in_map = pos in self.game.map.world_map
        #     pos_in_res_area = pos in self.restricted_area
        #
        # self.add_enemy(CacoDemon(self.game, pos=(x + 0.5, y + 0.5)))

    def spawn_sprites(self):
        # TODO this is just a convenience method for now that adds some sprites
        # but we'll really want to load sprites with the map/level
        green_light = 'assets/sprites/animated_sprites/green_light/0.png'
        red_light = 'assets/sprites/animated_sprites/red_light/0.png'
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
        pass

    def check_win(self):
        if not len(self.enemy_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        self.enemy_positions = {
            npc.map_pos
            for npc in self.enemy_list if npc.alive
        }
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.enemy_list]
        self.check_win()

    def add_enemy(self, enemy: Optional[Enemy]):
        if enemy:
            self.enemy_list.append(enemy)

    def add_sprite(self, sprite: Optional[Sprite]):
        if sprite:
            self.sprite_list.append(sprite)
