import json
import os
import pygame_menu as pm
from typing import Optional

from engine import RGBColors
from game import util


class LoadGameMenu:

    def __init__(self, main_menu: pm.Menu):
        self.main_menu: pm.Menu = main_menu
        self.menu: pm.Menu = pm.Menu(title="Load Game",
                                     width=main_menu.get_width(),
                                     height=main_menu.get_height(),
                                     theme=pm.themes.THEME_DARK)
        self.saves: list[tuple[str, int]] = []
        self.__save_data: Optional[dict] = None

    def _load_save_games(self):
        save_dir = util.get_user_save_game_path()
        all_files = os.listdir(save_dir)
        all_saves = [f for f in all_files if os.path.splitext(f)[1] == ".sav"]
        save_names = [os.path.splitext(f)[0] for f in all_saves]
        for i in range(len(save_names)):
            self.saves.append((save_names[i], i))

    def _load_game(self):
        data = self.menu.get_input_data()
        sel_idx = data['save_game_select'][1]
        if sel_idx is None:
            return

        # Get save game selection and determine file path.
        save_name = self.saves[sel_idx][0]
        save_dir = util.get_user_save_game_path()
        save_file = os.path.join(save_dir, f'{save_name}.sav')

        # Open the file if it exists
        if os.path.exists(save_file):
            print(f'Loading save game data: {save_file} ...')
            with open(save_file, encoding='UTF-8') as file:
                # Read the JSON data into a dict
                self.__save_data = json.load(file)
            self.main_menu.disable()

    def setup(self):
        self._load_save_games()
        self.menu.get_theme().widget_font_size = 20
        self.menu.get_theme().widget_font_color = RGBColors.WHITE.value
        self.menu.get_theme().widget_alignment = pm.locals.ALIGN_LEFT
        if self.saves:
            self.menu.add.dropselect(title="Select Save",
                                     default=0,
                                     items=self.saves,
                                     dropselect_id='save_game_select')
            self.menu.add.label(title="")
            self.menu.add.button(title="Load",
                                 action=self._load_game,
                                 font_color=RGBColors.WHITE.value,
                                 background_color=RGBColors.RED.value,
                                 align=pm.locals.ALIGN_CENTER)
        else:
            self.menu.add.label(title="No saved games found")

    def get_current(self) -> pm.Menu:
        return self.menu

    def get_selected_save_game_data(self) -> dict:
        return self.__save_data
