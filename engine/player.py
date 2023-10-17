import math
import pygame as pg
from typing import Optional

from engine import constants as con
from engine.input_handler import InputEvent
from engine.input_handler import Movement


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x: float = con.PLAYER_POS[0]
        self.y: float = con.PLAYER_POS[1]
        self.angle: int = con.PLAYER_ANGLE
        self.shot: bool = False
        self.health: int = con.PLAYER_MAX_HEALTH
        self.armor: int = 0
        self.rel: int = 0
        self.health_recovery_delay: int = 700
        self.time_prev: int = pg.time.get_ticks()
        self.diag_move_corr: float = 1 / math.sqrt(2)
        self.pain_sound: Optional[pg.mixer.Sound] = self.game.sound.player_pain
        self.movement_sound: Optional[pg.mixer.Sound] = \
            self.game.sound.player_movement
        self.do_continuous_fire: bool = False
        self.interact: bool = False
        self.sprite: pg.Surface = pg.Surface(((con.GRID_BLOCK / 12) - 6,
                                              (con.GRID_BLOCK / 12) - 6))
        self.rect: pg.Rect = self.sprite.get_rect()
        self.rect.center = (self.rect.width / 2, self.rect.height / 2)
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_pickup: bool = False

    def reset(self):
        self.x = con.PLAYER_POS[0]
        self.y = con.PLAYER_POS[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = con.PLAYER_ANGLE
        self.shot = False
        self.health = con.PLAYER_MAX_HEALTH
        self.rel = 0
        self.time_prev = pg.time.get_ticks()
        self.do_continuous_fire = False
        self.interact = False

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @property
    def map_pos(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def check_health_recovery_delay(self) -> bool:
        time_now = pg.time.get_ticks()
        delta = time_now - self.time_prev
        if delta > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        return False

    def recover_health(self):
        can_recover = self.health < con.PLAYER_MAX_HEALTH
        if self.check_health_recovery_delay() and can_recover:
            self.health += 1

    def give_health(self, health: int) -> bool:
        if self.health == con.PLAYER_MAX_HEALTH:
            return False

        print(f'Player took health: {health}%')
        if health > con.PLAYER_MAX_HEALTH:
            health = con.PLAYER_MAX_HEALTH

        if health < 1:
            health = 1

        if (self.health + health) > con.PLAYER_MAX_HEALTH:
            self.health = con.PLAYER_MAX_HEALTH
        else:
            self.health += health

        return True

    def give_armor(self, armor: int) -> bool:
        if self.armor == con.PLAYER_MAX_ARMOR:
            return False

        print(f'Player: took armor: {armor}%')
        if armor > con.PLAYER_MAX_ARMOR:
            armor = con.PLAYER_MAX_ARMOR

        if armor < 1:
            armor = 1

        if (self.armor + armor) > con.PLAYER_MAX_ARMOR:
            self.armor = con.PLAYER_MAX_ARMOR
        else:
            self.armor += armor

        return True

    def check_game_over(self):
        if self.health < 1:
            print('Player died!')
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def take_damage(self, damage: int):
        if not con.GOD_MODE:
            # If we have armor, decrement that first (but take double)
            if self.armor > 0:
                damage *= 2
                print(f'Armor damage: {damage}%')
                self.armor -= damage
                if self.armor < 0:
                    self.armor = 0
            else:
                print(f'Health damage: {damage}%')
                self.health -= damage
        self.game.object_renderer.player_damage()
        self.play_pain_sound()
        self.check_game_over()

    def check_do_continuous_fire(self):
        if (self.do_continuous_fire and
                self.game.current_weapon.frame_counter == 0):
            self.game.current_weapon.fire()

    def start_weapon_fire(self):
        self.do_continuous_fire = self.game.current_weapon.has_continuous_fire
        self.game.current_weapon.fire()

    def stop_weapon_fire(self):
        self.do_continuous_fire = False

    def single_fire_event(self, events: set[InputEvent]):
        start_fire = InputEvent.WEAPON_FIRE in events
        reloading = self.game.current_weapon.reloading
        if start_fire and not self.shot and not reloading:
            self.start_weapon_fire()

        stop_fire = InputEvent.WEAPON_FIRE_STOP in events
        if stop_fire:
            self.stop_weapon_fire()

    def check_wall(self, x: int, y: int) -> bool:
        return ((x, y) not in self.game.map.world_map and
                not self.game.map.has_obstacle((x, y)))

    def check_wall_collision(self, dx: float, dy: float):
        scale = con.PLAYER_SIZE_SCALE / self.game.delta_time
        x = int(self.x + dx * scale)
        y = int(self.y)
        if self.check_wall(x, y):
            self.x += dx

        x = int(self.x)
        y = int(self.y + dy * scale)
        if self.check_wall(x, y):
            self.y += dy

    def play_movement_sound(self):
        b_chan = self.game.sound.body_channel
        if self.movement_sound and not b_chan.get_busy():
            b_chan.play(self.movement_sound)

    def movement(self):
        movement = self.game.input.get_player_movement()

        dx = 0
        dy = 0
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = con.PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        num_key_pressed = -1
        if Movement.FORWARD in movement:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if Movement.BACKWARD in movement:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if Movement.LEFT in movement:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if Movement.RIGHT in movement:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        if movement:
            print(f'Player X = {self.x}, Y = {self.y}')
            self.rect.x = self.x
            self.rect.y = self.y
            self.play_movement_sound()

        # diagonal movement correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        if Movement.LOOK_LEFT in movement:
            self.angle -= con.PLAYER_ROT_SPEED * self.game.delta_time
        if Movement.LOOK_RIGHT in movement:
            self.angle += con.PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def draw(self):
        s_x = self.x * 100
        s_y = self.y * 100
        pg.draw.line(self.game.screen, 'yellow', (s_x, s_y),
                     (s_x + con.WIDTH * math.cos(self.angle),
                      s_y + con.WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (s_x, s_y), 15)

    def mouse_control(self):
        movement = self.game.input.get_mouse_movement()
        if movement:
            rel, angle = movement
            self.rel = rel
            self.angle += angle

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()
        self.check_do_continuous_fire()

    def play_pain_sound(self):
        if self.pain_sound:
            self.game.sound.play_sound(self.pain_sound)
