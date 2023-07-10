from enum import Enum
import pygame as pg
from typing import Optional

from engine import constants as con


class Movement(Enum):
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2
    RIGHT = 3
    LOOK_LEFT = 4
    LOOK_RIGHT = 5


class InputEvent(Enum):
    SCREENSHOT = 0
    PAUSE = 1
    TOGGLE_FULLSCREEN = 2
    QUIT = 3
    INTERACT = 4
    WEAPON_SWITCH = 5
    WEAPON_FIRE = 6
    WEAPON_FIRE_STOP = 7
    GLOBAL_EVENT = 8


class InputHandler:

    def __init__(self, game):
        self.game = game
        self.joystick_id: int = 0
        self.all_joysticks: list[pg.joystick.Joystick] = []
        self.mouse_sensitivity: float = con.MOUSE_SENSITIVITY
        self.mouse_fire_button: int = 1
        self.joy_fire_button: int = 0
        self.joy_pause_button: int = 6
        self.joy_quit_button: int = 4
        self.joy_use_button: int = 2
        self.joy_weapon_switch: int = 1
        self.joy_left_bumper: int = 9
        self.joy_right_bumper: int = 10
        self.joy_d_pad_x_axis: int = 0
        self.joy_d_pad_y_axis: int = 1
        pg.mouse.set_visible(con.DEBUG)
        pg.event.set_grab(True)

    @property
    def joystick(self) -> Optional[pg.joystick.Joystick]:
        if self.all_joysticks:
            return self.all_joysticks[self.joystick_id]
        return None

    def setup(self):
        self.all_joysticks = [
            pg.joystick.Joystick(x)
            for x in range(pg.joystick.get_count())
        ]

        [print(f'Found joystick: {j.get_name()}') for j in self.all_joysticks]

    def get_mouse_movement(self) -> Optional[tuple[int, int]]:
        if not pg.mouse.get_focused():
            return None

        mx, my = pg.mouse.get_pos()
        if mx < con.MOUSE_BORDER_LEFT or mx > con.MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([con.HALF_WIDTH, con.HALF_HEIGHT])

        rel = pg.mouse.get_rel()[0]
        rel = max(-con.MOUSE_MAX_REL, min(con.MOUSE_MAX_REL, rel))
        angle = rel * self.mouse_sensitivity * self.game.delta_time
        return rel, angle

    def get_player_movement(self) -> set[Movement]:
        keys = pg.key.get_pressed()
        joy = self.joystick
        joy_left_bump = joy.get_button(self.joy_left_bumper) if joy else False
        joy_right_bump = joy.get_button(self.joy_right_bumper) if joy else False
        d_pad_right = joy.get_axis(self.joy_d_pad_x_axis) >= 0.5 if joy else False
        d_pad_left = joy.get_axis(self.joy_d_pad_x_axis) <= -1 if joy else False
        d_pad_down = joy.get_axis(self.joy_d_pad_y_axis) >= 0.5 if joy else False
        d_pad_up = joy.get_axis(self.joy_d_pad_y_axis) <= -1 if joy else False
        # TODO support axis inversion for those weird southpaws ;-)

        result = set()
        if keys[pg.K_w] or d_pad_up:
            result.add(Movement.FORWARD)
        if keys[pg.K_s] or d_pad_down:
            result.add(Movement.BACKWARD)
        if keys[pg.K_a] or d_pad_left:
            result.add(Movement.LEFT)
        if keys[pg.K_d] or d_pad_right:
            result.add(Movement.RIGHT)
        if keys[pg.K_LEFT] or joy_left_bump:
            result.add(Movement.LOOK_LEFT)
        if keys[pg.K_RIGHT] or joy_right_bump:
            result.add(Movement.LOOK_RIGHT)

        return result

    def get_input_events(self) -> set[InputEvent]:
        result = set()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    result.add(InputEvent.SCREENSHOT)
                elif event.key == pg.K_p:
                    result.add(InputEvent.PAUSE)
                elif event.key == pg.K_t:
                    result.add(InputEvent.TOGGLE_FULLSCREEN)
                elif event.key == pg.K_ESCAPE:
                    result.add(InputEvent.QUIT)
                elif event.key == pg.K_e:
                    result.add(InputEvent.INTERACT)
                elif event.key == pg.K_SPACE:
                    result.add(InputEvent.WEAPON_FIRE)
                elif event.key == pg.K_TAB:
                    result.add(InputEvent.WEAPON_SWITCH)
            elif event.type == pg.JOYBUTTONDOWN:
                if event.button == self.joy_pause_button:
                    result.add(InputEvent.PAUSE)
                elif event.button == self.joy_quit_button:
                    result.add(InputEvent.QUIT)
                elif event.button == self.joy_use_button:
                    result.add(InputEvent.INTERACT)
                elif event.button == self.joy_fire_button:
                    result.add(InputEvent.WEAPON_FIRE)
                elif event.button == self.joy_weapon_switch:
                    result.add(InputEvent.WEAPON_SWITCH)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == self.mouse_fire_button:
                    result.add(InputEvent.WEAPON_FIRE)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    result.add(InputEvent.WEAPON_FIRE_STOP)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == self.mouse_fire_button:
                    result.add(InputEvent.WEAPON_FIRE_STOP)
            elif event.type == pg.JOYBUTTONUP:
                if event.button == self.joy_fire_button:
                    result.add(InputEvent.WEAPON_FIRE_STOP)
            elif event.type == pg.QUIT:
                result.add(InputEvent.QUIT)
            elif event.type == self.game.global_event:
                result.add(InputEvent.GLOBAL_EVENT)
        return result
