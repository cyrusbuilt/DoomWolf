from engine.enemy import Enemy
from engine.object_handler import ObjectHandler
from enemy import EnemyClass
from enemy.builder import EnemyBuilder


class DoomWolfObjectHandler(ObjectHandler):

    def __init__(self, game):
        super().__init__(game)

    def build_enemy_npc(self, game, klass: EnemyClass, pos: tuple[float, float]) -> Enemy:
        # TODO replace this with logic to load enemy descriptor via factory method
        return EnemyBuilder.build_enemy(game, klass, pos)
