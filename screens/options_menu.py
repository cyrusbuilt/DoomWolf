import pygame as pg
import pygame_menu as pm
from typing import Optional

from engine import Resolution
from engine import RGBColors
from game.settings import GameSettings


class OptionsMenu:

    def __init__(self, path: str, width: int, height: int):
        self.menu: pm.Menu = pm.Menu(title="Options",
                                     width=width,
                                     height=height,
                                     theme=pm.themes.THEME_DARK)
        self.joy_menu: Optional[pm.Menu] = None
        self.mouse_menu: Optional[pm.Menu] = None
        self.settings: GameSettings = GameSettings(path)
        self.display_modes: list[tuple[str, Resolution]] = []
        self.res_drop: Optional[pm.widgets.DropSelect] = None

    def save_options(self):
        data = self.menu.get_input_data()
        for key in data.keys():
            if key == "launch_fullscreen":
                self.settings.launch_fullscreen = data[key]
            elif key == "music_volume":
                self.settings.music_volume = round(data[key], 1)
            elif key == "monitor_id":
                self.settings.monitor_id = data[key][0][1]
            elif key == "resolution":
                self.settings.resolution = data[key][0][1]
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

    @staticmethod
    def _get_monitor_ids() -> list[tuple[str, int]]:
        return [(str(x), x) for x in range(pg.display.get_num_displays())]

    @staticmethod
    def _get_display_modes_for_monitor(monitor: int) -> list[tuple[str, Resolution]]:
        return [(f'{str(x[0])}x{str(x[1])}', Resolution.from_tuple(x))
                for x in pg.display.list_modes(display=monitor)]

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
        def_joy_id = self.settings.joy_id
        all_joys = self._get_joystick_ids()
        joy_count = len(all_joys)
        if joy_count == 0:
            def_joy_id = None
        elif def_joy_id > joy_count - 1:
            def_joy_id = 0

        joy_name = "< No joystick/gamepad detected >"
        if def_joy_id is not None:
            curr_joy = pg.joystick.Joystick(def_joy_id)
            joy_name = curr_joy.get_name()
            joy_menu.add.dropselect(title="Gamepad/Joystick ID",
                                    default=def_joy_id,
                                    items=all_joys,
                                    dropselect_id='joy_id')
        joy_menu.add.label(title=f'Current: {joy_name}')
        if def_joy_id is None:
            return joy_menu

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

    def _get_selected_monitor(self) -> int:
        data = self.menu.get_input_data()
        if 'monitor_id' not in data:
            return 0
        return data['monitor_id'][0][1]

    def _update_display_modes(self):
        monitor = self._get_selected_monitor()
        self.display_modes = self._get_display_modes_for_monitor(monitor)
        found_1600: bool = False
        for res in self.display_modes:
            if res[0] == "1600x900":
                found_1600 = True
                break

        if not found_1600:
            self.display_modes.append(("1600x900", Resolution(1600, 900)))

        if self.res_drop:
            self.res_drop.update_items(self.display_modes)

    def _on_res_change(self, *args, **kwargs):
        self._update_display_modes()

    def setup(self):
        self.settings.load_settings()
        self.menu.get_theme().widget_font_size = 20
        self.menu.get_theme().widget_font_color = RGBColors.WHITE.value
        self.menu.get_theme().widget_alignment = pm.locals.ALIGN_LEFT

        monitor_ids = self._get_monitor_ids()
        default_disp_index: int = self.settings.monitor_id
        mon_count = len(monitor_ids)
        if default_disp_index > mon_count - 1:
            default_disp_index = 0

        disp_index: int = 0
        for res in self.display_modes:
            if res[1] == self.settings.resolution:
                default_disp_index = disp_index
                break
            disp_index += 1

        # TODO Need option for sounds toggle
        self.menu.add.dropselect(title="Display",
                                 default=default_disp_index,
                                 items=monitor_ids,
                                 dropselect_id='monitor_id',
                                 onchange=self._on_res_change)
        self._update_display_modes()
        self.res_drop = self.menu.add.dropselect(title="Resolution",
                                                 default=default_disp_index,
                                                 items=self.display_modes,
                                                 dropselect_id='resolution')
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
