import json
import os

from engine import constants as con


class GameSettings:

    def __init__(self, path: str):
        self.path: str = path
        self.music_volume: float = 0.4
        self.launch_fullscreen: bool = False
        self.mouse_sensitivity: float = con.MOUSE_SENSITIVITY

    def to_dict(self) -> dict:
        return {
            'music_volume': self.music_volume,
            'launch_fullscreen': self.launch_fullscreen,
            'input': {
                'mouse_sensitivity': self.mouse_sensitivity
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
                    mouse_sens = user_input.get('mouse_sensitivity')
                    if mouse_sens:
                        self.mouse_sensitivity = mouse_sens

        else:
            print('ERROR: Settings file not found!')

    def save_settings(self):
        with open(self.path, 'w') as file:
            json.dump(self.to_dict(), file)
