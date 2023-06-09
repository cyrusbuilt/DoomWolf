from enemy import EnemyBase
from enemy import EnemyClass


class CyberDemon(EnemyBase):

    def __init__(self,
                 game,
                 path: str = 'assets/sprites/enemy/cyber_demon/0.png',
                 pos: tuple[float, float] = (11.5, 6.0),
                 scale: float = 1.0,
                 shift: float = 0.04,
                 animation_time: int = 210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.enemy_class = EnemyClass.CYBER_DEMON
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
