from enum import Enum

from engine.weapon import Weapon


class WeaponClass(Enum):
    SHOTGUN = 'shotgun'
    CHAINSAW = 'chainsaw'
    NONE = 'none'


class WeaponBase(Weapon):

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class: WeaponClass = WeaponClass.NONE
