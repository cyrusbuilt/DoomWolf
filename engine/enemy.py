from collections import deque
import math
import os
import pygame as pg
from random import randint, random

from engine import constants as con
from engine.sprite import AnimatedSprite


class Enemy(AnimatedSprite):

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (10.5, 5.5),
                 scale: float = 0.6,
                 shift: float = 0.38,
                 animation_time: int = 180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.name: str = ''
        self.attack_images: deque[pg.Surface] = deque()
        self.death_images: deque[pg.Surface] = deque()
        self.idle_images: deque[pg.Surface] = deque()
        self.pain_images: deque[pg.Surface] = deque()
        self.walk_images: deque[pg.Surface] = deque()
        self.see_images: deque[pg.Surface] = deque()
        self.attack_dist: int = randint(3, 6)
        self.speed: float = 0.03
        self.size: int = 20
        self.health: int = 100
        self.attack_damage: int = 10
        self.accuracy: float = 0.15
        self.alive: bool = True
        self.pain: bool = False
        self.ray_cast_value: bool = False
        self.frame_counter: int = 0
        self.player_search_trigger: bool = False
        self.spawn_weight: int = 0
        self.sounds: dict[str, pg.mixer.Sound] = {}

    @property
    def id(self) -> str:
        return f'{self.name}_{int(self.x)}_{int(self.y)}'

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def setup(self):
        self.attack_images = self.load_images(os.path.join(self.path, "attack"))
        self.death_images = self.load_images(os.path.join(self.path, "death"))
        self.idle_images = self.load_images(os.path.join(self.path, "idle"))
        self.pain_images = self.load_images(os.path.join(self.path, "pain"))
        self.walk_images = self.load_images(os.path.join(self.path, "walk"))
        self.see_images = self.load_images(os.path.join(self.path, "see"))

    def check_wall(self, x: int, y: int) -> bool:
        return ((x, y) not in self.game.map.world_map and
                not self.game.map.has_obstacle((x, y)))

    def check_wall_collision(self, dx: float, dy: float):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def play_action_sound(self, action: str):
        action_sound = self.sounds.get(action)
        if action_sound:
            self.game.sound.play_sound(action_sound)
        else:
            print(f"ERROR: Sound not found for action: '{action}'")

    def movement(self):
        # TODO check collision with player and/or vice-versa. Currently, the player can literally walk through
        # enemies. We need to prevent this.
        get_path = self.game.path_finder.get_path
        my_pos = self.map_pos
        player_pos = self.game.player.map_pos
        next_pos = get_path(my_pos, player_pos)
        next_x, next_y = next_pos

        if con.DEBUG:
            d_rect = (100 * next_x, 100 * next_y, 100, 100)
            pg.draw.rect(self.game.screen, 'blue', d_rect)

        if next_pos not in self.game.object_handler.enemy_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.play_action_sound('attack')
            if random() < self.accuracy:
                self.game.player.take_damage(self.attack_damage)

    def see_player(self):
        if self.animation_trigger:
            self.animate(self.see_images)
            self.play_action_sound('see')

    def animate_death(self):
        if not self.alive:
            good_frame = self.frame_counter < len(self.death_images) - 1
            if self.game.global_trigger and good_frame:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.play_action_sound('death')

    def check_damage(self):
        if self.ray_cast_value and self.game.player.shot:
            w1 = con.HALF_WIDTH - self.sprite_half_width
            w2 = con.HALF_WIDTH + self.sprite_half_width
            if w1 < self.screen_x < w2:
                self.play_action_sound('pain')
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.current_weapon.damage
                self.check_health()

    def ray_cast_enemy(self) -> bool:
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v = 0
        wall_dist_h = 0
        player_dist_v = 0
        player_dist_h = 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for _ in range(con.MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            if tile_hor in self.game.map.obstacles:
                # Treat obstacles the same as walls
                wall_dist_h = depth_hor
                break

            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for _ in range(con.MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            if tile_vert in self.game.map.obstacles:
                # Treat obstacles the same as walls
                wall_dist_v = depth_vert
                break

            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        center = (100 * self.x, 100 * self.y)
        pg.draw.circle(self.game.screen, 'red', center, 15)
        if self.ray_cast_enemy():
            p = self.game.player
            player_center = (100 * p.x, 100 * p.y)
            pg.draw.line(self.game.screen, 'orange', player_center, center, 2)

    def think(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_enemy()
            self.check_damage()

            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value and not self.game.test_mode:
                # TODO In the future, we should probably implement a way for
                # enemies to 'lose track' of the player and go back to idle.
                # Right now, once an enemy spots the player, it *never* loses
                # track of the player. It's possible to attract the attention
                # of a whole bunch of enemies at once and have to battle them
                # all. While certainly a challenge, I could also see this as
                # annoying and impossible to survive (ie. multiple cyber
                # demons + soldiers attacking at once). We should have some
                # criteria/threshold where player_search_trigger and
                # ray_cast_value is reset to false.
                self.player_search_trigger = True
                self.see_player()

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    def update(self):
        self.check_animation_time()
        self.refresh_sprite()
        self.think()
        if con.DEBUG:
            self.draw_ray_cast()
