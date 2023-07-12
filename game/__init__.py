from game.doom_wolf import DoomWolf
from game.doom_wolf import SETTINGS
from screens.main_menu import MainMenu
from screens.options_menu import OptionsMenu


def run_doom_wolf(window_title: str = 'DoomWolf'):
    main_menu = MainMenu(window_title, 700, 800)

    options = OptionsMenu(SETTINGS, main_menu.width, main_menu.height)
    options.setup()

    main_menu.set_options_menu(options.get_current())
    main_menu.show_menu()

    dw = DoomWolf(window_title)
    dw.find_maps()
    dw.new_game()
    dw.run()
