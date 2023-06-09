from enemy import EnemyBase
from enemy import EnemyClass


class Soldier(EnemyBase):

    def __init__(self,
                 game,
                 path: str = 'assets/sprites/enemy/soldier/0.png',
                 pos: tuple[float, float] = (10.5, 5.5),
                 scale: float = 0.6,
                 shift: float = 0.38,
                 animation_time: int = 180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.enemy_class = EnemyClass.SOLDIER
