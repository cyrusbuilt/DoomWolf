from enemy import EnemyBase
from enemy import EnemyClass


class CacoDemon(EnemyBase):

    def __init__(self,
                 game,
                 path: str = 'assets/sprites/enemy/caco_demon/0.png',
                 pos: tuple[float, float] = (10.5, 6.5),
                 scale: float = 0.7,
                 shift: float = 0.27,
                 animation_time: int = 250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.enemy_class = EnemyClass.CACO_DEMON
        self.attack_dist = 1
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35
