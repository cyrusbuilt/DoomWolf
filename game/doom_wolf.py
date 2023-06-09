from engine.game import Game
from weapon.weapon_inventory import WeaponInventory


class DoomWolf(Game):

    def __init__(self, window_title: str = 'DoomWolf'):
        super().__init__()
        self.window_title = window_title
        self.weapon_inventory: WeaponInventory = WeaponInventory(self)

    def new_game(self):
        super().new_game()
        self.current_weapon = self.weapon_inventory.get_current()
