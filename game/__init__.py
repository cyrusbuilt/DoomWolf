import os
import shutil

from game import util
from game.doom_wolf import DoomWolf
from game.doom_wolf import SETTINGS
from game.settings import GameSettings
from screens.main_menu import MainMenu
from screens.options_menu import OptionsMenu


def run_doom_wolf(window_title: str = 'DoomWolf'):
    # Create game data directory (if it doesn't already exist) and copy the
    # settings file there and load settings from there. That way the original
    # settings file is not modified. If the user hoses something up, they can
    # always just delete the settings folder from the game data folder in their
    # profile and restart the game to generate a new copy. However, if anything
    # goes wrong with this, fallback to using the settings file provided with
    # the game.
    dw_settings = GameSettings(SETTINGS)
    user_dw_path = util.get_user_game_data_path()
    os.makedirs(user_dw_path, exist_ok=True)
    if os.path.exists(SETTINGS) and os.path.exists(user_dw_path):
        user_game_settings = os.path.join(user_dw_path, SETTINGS)
        if not os.path.exists(user_game_settings):
            shutil.copyfile(SETTINGS, user_game_settings)
        dw_settings = GameSettings(user_game_settings)

    main_menu = MainMenu(window_title, 700, 625)

    options = OptionsMenu(dw_settings.path, main_menu.width, main_menu.height)
    options.setup()

    main_menu.set_options_menu(options.get_current())
    main_menu.show_menu()

    dw = DoomWolf(window_title, dw_settings)
    dw.find_maps()
    dw.new_game()
    dw.run()
