import os
import shutil

from game import util
from game.doom_wolf import DoomWolf
from game.doom_wolf import SETTINGS
from game.settings import GameSettings
from screens.load_game import LoadGameMenu
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

    game_load = LoadGameMenu(main_menu.get_current())
    game_load.setup()

    main_menu.set_options_menu(options.get_current())
    main_menu.set_load_game_menu(game_load.get_current())
    main_menu.show_menu()

    save_game = game_load.get_selected_save_game_data()

    dw = DoomWolf(window_title, dw_settings)
    dw.find_maps()
    if save_game:
        dw.load_game(save_game)
    else:
        dw.new_game()
    dw.run()


def test_map(map_path: str):
    if not os.path.isabs(map_path):
        print(f'ERROR: {map_path} is not an absolute path.')
        quit()

    dw_settings = GameSettings("")
    _, file_name = os.path.split(map_path)
    title = f'Testing map: {file_name}'
    dw = DoomWolf(title, dw_settings)
    dw.load_test_map(map_path)
    dw.new_game()
    dw.run()
