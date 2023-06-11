from weapon import WeaponBase
from weapon import WeaponClass


class Pistol(WeaponBase):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 3.0,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class = WeaponClass.PISTOL
        self.sound = game.sound.get_weapon_sound(self.weapon_class)
        self.damage = 40
