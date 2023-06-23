from engine import constants as con
from engine.enemy import Enemy
from engine.object_handler import ObjectHandler
from enemy import get_enemy_meta
from enemy import enemy


class DoomWolfObjectHandler(ObjectHandler):

    def __init__(self, game):
        super().__init__(game)
        self.enemy_paths: dict[str, str] = {}

    def setup(self):
        super().setup()
        data, paths = get_enemy_meta(con.ENEMY_DATA_BASE)
        items = data.items()
        spawn_weights = dict(sorted(items, key=lambda item: item[1], reverse=True))
        self.enemy_types = list(spawn_weights.keys())
        self.weights = list(spawn_weights.values())
        self.enemy_paths = paths

    def build_enemy_npc(self, game, klass: str, pos: tuple[float, float]) -> Enemy:
        path = self.enemy_paths[klass]
        return enemy(game, path, pos).build()
