from game.doom_wolf import DoomWolf


def run_doom_wolf(window_title: str = 'DoomWolf'):
    dw = DoomWolf(window_title)
    dw.find_maps()
    dw.new_game()
    dw.run()
