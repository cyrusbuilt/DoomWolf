import json
import os

from engine import constants as con


class GameSettings:

    def __init__(self, path: str):
        self.path: str = path
        self.music_volume: float = 0.4
        self.launch_fullscreen: bool = False
        self.mouse_sensitivity: float = con.MOUSE_SENSITIVITY
        self.mouse_fire_button: int = 1
        self.joy_id: int = 0
        self.joy_fire_button: int = 0
        self.joy_pause_button: int = 6
        self.joy_quit_button: int = 4
        self.joy_use_button: int = 2
        self.joy_weapon_switch: int = 1
        self.joy_left_bumper: int = 9
        self.joy_right_bumper: int = 10
        self.joy_d_pad_x_axis: int = 0
        self.joy_d_pad_y_axis: int = 1

    def to_dict(self) -> dict:
        return {
            'music_volume': self.music_volume,
            'launch_fullscreen': self.launch_fullscreen,
            'input': {
                'mouse': {
                    'sensitivity': self.mouse_sensitivity,
                    'fire_button': self.mouse_fire_button
                },
                'joystick': {
                    'id': self.joy_id,
                    'fire_button': self.joy_fire_button,
                    'pause_button': self.joy_pause_button,
                    'quit_button': self.joy_quit_button,
                    'use_button': self.joy_use_button,
                    'weapon_switch_button': self.joy_weapon_switch,
                    'left_bumper_button': self.joy_left_bumper,
                    'right_bumper_button': self.joy_right_bumper,
                    'd-pad_x_axis': self.joy_d_pad_x_axis,
                    'd-pad_y_axis': self.joy_d_pad_y_axis
                }
            }
        }

    def load_settings(self):
        print(f'Loading settings file: {self.path}')
        if os.path.exists(self.path):
            with open(self.path, encoding='UTF-8') as file:
                settings = json.load(file)
                m_volume = settings.get('music_volume')
                if m_volume:
                    self.music_volume = m_volume

                fullscreen = settings.get('launch_fullscreen')
                if fullscreen:
                    self.launch_fullscreen = fullscreen

                user_input = settings.get('input')
                if user_input:
                    mouse_input = user_input.get('mouse')
                    if mouse_input:
                        mouse_sens = mouse_input.get('sensitivity')
                        if mouse_sens:
                            self.mouse_sensitivity = mouse_sens

                        self.mouse_fire_button = mouse_input.get('fire_button', 1)

                    joy_input = user_input.get('joystick')
                    if joy_input:
                        self.joy_id = joy_input.get('id', 0)
                        self.joy_fire_button = joy_input.get('fire_button', 0)
                        self.joy_pause_button = joy_input.get('pause_button', 6)
                        self.joy_quit_button = joy_input.get('quit_button', 4)
                        self.joy_use_button = joy_input.get('use_button', 2)
                        self.joy_weapon_switch = joy_input.get('weapon_switch_button', 1)
                        self.joy_left_bumper = joy_input.get('left_bumper_button', 9)
                        self.joy_right_bumper = joy_input.get('right_bumper_button', 10)
                        self.joy_d_pad_x_axis = joy_input.get('d-pad_x_axis', 0)
                        self.joy_d_pad_y_axis = joy_input.get('d-pad_y_axis', 1)
        else:
            print('ERROR: Settings file not found!')

    def save_settings(self):
        with open(self.path, 'w') as file:
            json.dump(self.to_dict(), file, indent=2)
        print(f'Saved settings to {self.path}')
