from typing import Optional

from enemy import EnemyBase
from enemy import EnemyClass
from enemy.caco_demon import CacoDemon
from enemy.cyber_demon import CyberDemon
from enemy.soldier import Soldier


class EnemyBuilder:

    @staticmethod
    def build_enemy(
        game, klass: EnemyClass,
        pos: tuple[float, float] = (10.5, 5.5)) -> Optional[EnemyBase]:
        if klass == EnemyClass.NONE:
            return None
        if klass == EnemyClass.CACO_DEMON:
            return CacoDemon(game=game, pos=pos)
        if klass == EnemyClass.CYBER_DEMON:
            return CyberDemon(game=game, pos=pos)
        if klass == EnemyClass.SOLDIER:
            return Soldier(game=game, pos=pos)
