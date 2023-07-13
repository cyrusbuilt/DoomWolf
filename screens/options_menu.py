import pygame as pg
import pygame_menu as pm
from typing import Optional

from game.settings import GameSettings
from screens import RGBColors


class OptionsMenu:

    def __init__(self, path: str, width: int, height: int):
        self.menu: pm.Menu = pm.Menu(title="Options",
                                     width=width,
                                     height=height,
                                     theme=pm.themes.THEME_DARK)
        self.joy_menu: Optional[pm.Menu] = None
        self.mouse_menu: Optional[pm.Menu] = None
        self.settings: GameSettings = GameSettings(path)

    def save_options(self):
        data = self.menu.get_input_data()
        for key in data.keys():
            if key == "launch_fullscreen":
                self.settings.launch_fullscreen = data[key]
            elif key == "music_volume":
                self.settings.music_volume = round(data[key], 1)
            else:
                print(f'WARN: Unrecognized options key: {key}')

        self.settings.save_settings()

    @staticmethod
    def _get_mouse_button_ids() -> list[tuple[str, int]]:
        return [(str(x), x) for x in range(4)]

    @staticmethod
    def _get_joystick_ids() -> list[tuple[str, int]]:
        return [(str(x), x) for x in range(pg.joystick.get_count())]

    @staticmethod
    def _get_joy_button_ids() -> list[tuple[str, int]]:
        return [(str(x), x) for x in range(11)]

    @staticmethod
    def _get_joy_axis_ids() -> list[tuple[str, int]]:
        return [(str(x), x) for x in range(2)]

    def _store_joy_settings(self):
        data = self.joy_menu.get_input_data()
        for key in data.keys():
            if key == "joy_id":
                self.settings.joy_id = data[key][0][1]
            elif key == "joy_fire_button":
                self.settings.joy_fire_button = data[key][0][1]
            elif key == "joy_pause_button":
                self.settings.joy_pause_button = data[key][0][1]
            elif key == "joy_quit_button":
                self.settings.joy_quit_button = data[key][0][1]
            elif key == "joy_use_button":
                self.settings.joy_use_button = data[key][0][1]
            elif key == "joy_weapon_switch":
                self.settings.joy_weapon_switch = data[key][0][1]
            elif key == "joy_left_bumper":
                self.settings.joy_left_bumper = data[key][0][1]
            elif key == "joy_right_bumper":
                self.settings.joy_right_bumper = data[key][0][1]
            elif key == "joy_d_pad_x_axis":
                self.settings.joy_d_pad_x_axis = data[key][0][1]
            elif key == "joy_d_pad_y_axis":
                self.settings.joy_d_pad_y_axis = data[key][0][1]
            else:
                print(f'WARN: Unrecognized options key: {key}')

    def _joystick_options(self) -> pm.Menu:
        joy_menu: pm.Menu = pm.Menu(title='Joystick Options',
                                    width=self.menu.get_width(),
                                    height=self.menu.get_height(),
                                    theme=self.menu.get_theme())
        self.joy_menu = joy_menu
        joy_menu.add.dropselect(title="Gamepad/Joystick ID",
                                default=self.settings.joy_id,
                                items=self._get_joystick_ids(),
                                dropselect_id='joy_id')
        joy_menu.add.dropselect(title="Gamepad Fire Button",
                                default=self.settings.joy_fire_button,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_fire_button')
        joy_menu.add.dropselect(title='Gamepad Pause Button',
                                default=self.settings.joy_pause_button,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_pause_button')
        joy_menu.add.dropselect(title="Gamepad Quit Button",
                                default=self.settings.joy_quit_button,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_quit_button')
        joy_menu.add.dropselect(title="Gamepad Use Button",
                                default=self.settings.joy_use_button,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_use_button')
        joy_menu.add.dropselect(title="Gamepad Weapon Switch",
                                default=self.settings.joy_weapon_switch,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_weapon_switch')
        joy_menu.add.dropselect(title="Gamepad Left Bumper",
                                default=self.settings.joy_left_bumper,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_left_bumper')
        joy_menu.add.dropselect(title="Gamepad Right Bumper",
                                default=self.settings.joy_right_bumper,
                                items=self._get_joy_button_ids(),
                                dropselect_id='joy_right_bumper')
        joy_menu.add.dropselect(title="Gamepad D-Pad X-axis",
                                default=self.settings.joy_d_pad_x_axis,
                                items=self._get_joy_axis_ids(),
                                dropselect_id='joy_d_pad_x_axis')
        joy_menu.add.dropselect(title="Gamepad D-Pad Y-axis",
                                default=self.settings.joy_d_pad_y_axis,
                                items=self._get_joy_axis_ids(),
                                dropselect_id='joy_d_pad_y_axis')
        joy_menu.add.label(title="")
        joy_menu.add.button(title="Save",
                            action=pm.events.BACK,
                            onselect=self._store_joy_settings,
                            font_color=RGBColors.WHITE.value,
                            background_color=RGBColors.RED.value,
                            align=pm.locals.ALIGN_CENTER,
                            button_id='joy_options_save')
        return joy_menu

    def _store_mouse_options(self):
        data = self.mouse_menu.get_input_data()
        for key in data:
            if key == "mouse_sensitivity":
                self.settings.mouse_sensitivity = round(data[key], 4)
            elif key == "mouse_fire_button":
                self.settings.mouse_fire_button = data[key][0][1]
            else:
                print(f'WARN: Unrecognized options key: {key}')

    def _mouse_options(self) -> pm.Menu:
        mouse_menu: pm.Menu = pm.Menu(title='Mouse Options',
                                      width=self.menu.get_width(),
                                      height=self.menu.get_height(),
                                      theme=self.menu.get_theme())
        self.mouse_menu = mouse_menu
        mouse_menu.add.range_slider(title='Mouse Sensitivity',
                                    default=self.settings.mouse_sensitivity,
                                    rangeslider_id='mouse_sensitivity',
                                    increment=0.0001,
                                    range_values=(0.0, 0.1))
        mouse_menu.add.dropselect(title='Mouse Fire Button',
                                  default=self.settings.mouse_fire_button,
                                  items=self._get_mouse_button_ids(),
                                  dropselect_id='mouse_fire_button')
        mouse_menu.add.label("")
        mouse_menu.add.button(title="Save",
                              action=pm.events.BACK,
                              onselect=self._store_mouse_options,
                              font_color=RGBColors.WHITE.value,
                              background_color=RGBColors.RED.value,
                              align=pm.locals.ALIGN_CENTER,
                              button_id='mouse_options_save')
        return mouse_menu

    def setup(self):
        self.settings.load_settings()
        self.menu.get_theme().widget_font_size = 20
        self.menu.get_theme().widget_font_color = RGBColors.WHITE.value
        self.menu.get_theme().widget_alignment = pm.locals.ALIGN_LEFT
        # TODO Need options for screen res and sounds toggle
        self.menu.add.toggle_switch(title="Launch full screen",
                                    default=self.settings.launch_fullscreen,
                                    toggleswitch_id="launch_fullscreen")
        self.menu.add.range_slider(title="Music Volume",
                                   default=self.settings.music_volume,
                                   rangeslider_id='music_volume',
                                   increment=0.1,
                                   range_values=(0.0, 1.0))
        self.menu.add.label(title="")
        self.menu.add.button(title='Joystick/Gamepad',
                             button_id='joystick',
                             action=self._joystick_options(),
                             font_color=RGBColors.WHITE.value,
                             background_color=RGBColors.RED.value,
                             align=pm.locals.ALIGN_CENTER)
        self.menu.add.label(title="")
        self.menu.add.button(title='Mouse',
                             button_id='mouse',
                             action=self._mouse_options(),
                             font_color=RGBColors.WHITE.value,
                             background_color=RGBColors.RED.value,
                             align=pm.locals.ALIGN_CENTER)
        self.menu.add.label(title="")
        self.menu.add.button(title='Save',
                             onselect=self.save_options,
                             action=pm.events.BACK,
                             font_color=RGBColors.WHITE.value,
                             background_color=RGBColors.RED.value,
                             align=pm.locals.ALIGN_CENTER)

    def get_current(self) -> pm.Menu:
        return self.menu
