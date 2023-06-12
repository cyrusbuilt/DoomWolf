from enum import Enum

from engine.weapon import Weapon


class WeaponClass(Enum):
    PISTOL = 'pistol'
    SHOTGUN = 'shotgun'
    CHAINSAW = 'chainsaw'
    SUPER_SHOTGUN = 'super_shotgun'
    NONE = 'none'


class WeaponBase(Weapon):
    # TODO Need to completely rethink this. Instead of adding new members
    # to the enum and making new subclasses for each new type of weapon,
    # maybe just have the generic weapon class support all variables,
    # event hooks, etc and then declare it's type as string (for unique
    # identification and to help locate assets) and then load all the
    # variables from a JSON file. This will making modding easier and
    # make introducing new weapons as easy as writing a new JSON file.
    # We'll keep using the existing system for now though to help determine
    # what all needs to go into the JSON schema.

    def __init__(self,
                 game,
                 path: str,
                 scale: float = 0.4,
                 animation_time: int = 90):
        super().__init__(game, path, scale, animation_time)
        self.weapon_class: WeaponClass = WeaponClass.NONE
