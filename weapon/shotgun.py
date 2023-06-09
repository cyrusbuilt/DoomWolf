from weapon import WeaponBase
from weapon import WeaponClass


class Shotgun(WeaponBase):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class = WeaponClass.SHOTGUN
        self.sound = game.sound.get_weapon_sound(self.weapon_class)
