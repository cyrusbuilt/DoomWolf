from enum import Enum
from typing import Optional

from engine.enemy import Enemy


class EnemyClass(Enum):
    SOLDIER = 'soldier'
    CACO_DEMON = 'caco_demon'
    CYBER_DEMON = 'cyber_demon'
    NONE = 'none'


class EnemyBase(Enemy):

    def __init__(self,
                 game,
                 path: str,
                 pos: tuple[float, float] = (10.5, 5.5),
                 scale: float = 0.6,
                 shift: float = 0.38,
                 animation_time: int = 180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.enemy_class: EnemyClass = EnemyClass.NONE
