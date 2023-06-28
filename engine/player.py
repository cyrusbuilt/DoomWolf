import math
import pygame as pg
from typing import Optional

from engine import constants as con


class Player:

    def __init__(self, game):
        self.game = game
        self.x: float = con.PLAYER_POS[0]
        self.y: float = con.PLAYER_POS[1]
        self.angle: int = con.PLAYER_ANGLE
        self.shot: bool = False
        self.health: int = con.PLAYER_MAX_HEALTH
        self.rel: int = 0
        self.health_recovery_delay: int = 700
        self.time_prev: int = pg.time.get_ticks()
        self.diag_move_corr: float = 1 / math.sqrt(2)
        self.pain_sound: Optional[pg.mixer.Sound] = self.game.sound.player_pain
        self.do_continuous_fire: bool = False

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

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def take_damage(self, damage: int):
        if not con.GOD_MODE:
            self.health -= damage
        self.game.object_renderer.player_damage()
        self.play_pain_sound()
        self.check_game_over()

    def check_do_continuous_fire(self):
        if self.do_continuous_fire:
            if self.game.current_weapon.frame_counter == 0:
                self.game.current_weapon.play_attack_sound()
                self.shot = True
                self.game.current_weapon.reloading = True

    def start_weapon_fire(self):
        self.do_continuous_fire = self.game.current_weapon.has_continuous_fire
        self.game.current_weapon.play_attack_sound()
        self.shot = True
        self.game.current_weapon.reloading = True

    def stop_weapon_fire(self):
        self.do_continuous_fire = False

    def single_fire_event(self, event: pg.event.Event):
        mouse_fire = event.type == pg.MOUSEBUTTONDOWN and \
                     event.button == 1
        joy_fire = event.type == pg.JOYBUTTONDOWN and \
                   event.button == 0
        kbd_fire = event.type == pg.KEYDOWN and \
                   event.key == pg.K_SPACE

        if (mouse_fire or joy_fire or kbd_fire) and not self.shot and \
                not self.game.current_weapon.reloading:
            self.start_weapon_fire()

        mouse_fire_stop = event.type == pg.MOUSEBUTTONUP and \
                          event.button == 1
        joy_fire_stop = event.type == pg.JOYBUTTONUP and \
                        event.button == 0
        kbd_fire_stop = event.type == pg.KEYUP and \
                        event.key == pg.K_SPACE

        if mouse_fire_stop or joy_fire_stop or kbd_fire_stop:
            self.stop_weapon_fire()

    def check_wall(self, x: int, y: int) -> bool:
        return (x, y) not in self.game.map.world_map

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

    def movement(self):
        keys = pg.key.get_pressed()
        joy_left_bump = self.game.joystick.get_button(9)
        joy_right_bump = self.game.joystick.get_button(10)
        d_pad_right = self.game.joystick.get_axis(0) >= 0.5
        d_pad_left = self.game.joystick.get_axis(0) <= -1
        d_pad_down = self.game.joystick.get_axis(1) >= 0.5
        d_pad_up = self.game.joystick.get_axis(1) <= -1

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx = 0
        dy = 0
        speed = con.PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        num_key_pressed = -1
        if keys[pg.K_w] or d_pad_up:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s] or d_pad_down:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a] or d_pad_left:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d] or d_pad_right:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diagonal movement correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT] or joy_left_bump:
            self.angle -= con.PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT] or joy_right_bump:
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
        mx, my = pg.mouse.get_pos()
        if mx < con.MOUSE_BORDER_LEFT or mx > con.MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([con.HALF_WIDTH, con.HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-con.MOUSE_MAX_REL, min(con.MOUSE_MAX_REL, self.rel))
        mouse_sens = self.game.mouse_sensitivity
        self.angle += self.rel * mouse_sens * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()
        self.check_do_continuous_fire()

    def play_pain_sound(self):
        if self.pain_sound:
            self.pain_sound.play()
