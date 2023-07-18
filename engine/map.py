import pygame as pg
from typing import Optional


_ = False

# yapf: disable
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]
# yapf: enable


class Map:

    def __init__(self, game, name: str):
        self.name: str = name
        self.mini_map: list[list[int] | list[int | bool]] = mini_map
        self.game = game
        self.world_map: dict[tuple[int, int], int] = {}
        self.obstacles: list[tuple[int, int]] = []
        self.rows: int = len(self.mini_map)
        self.cols: int = len(self.mini_map[0])
        self.sky_texture: Optional[pg.Surface] = None
        self.sky_offset: int = 0
        self.floor_texture: Optional[pg.Surface] = None
        self.floor_color: Optional[pg.Color] = None
        self.music_track: Optional[str] = None
        self.sprite_map_path: Optional[str] = None
        self.enemy_count: int = 0
        self.won: bool = False
        self.enemies: Optional[list[str]] = None

    def load_map(self):
        print(f'Loading map: {self.name}')
        if self.music_track:
            self.game.sound.music_path = self.music_track

        # TODO Load floor texture

        if self.floor_color:
            self.game.object_renderer.floor_color = self.floor_color

        if self.sky_texture:
            self.game.object_renderer.sky_image = self.sky_texture

        if self.enemy_count > 0:
            self.game.object_handler.enemy_count = self.enemy_count

        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [
            pg.draw.rect(self.game.screen, 'darkgray',
                         (pos[0] * 100, pos[1] * 100, 100, 100), 2)
            for pos in self.world_map
        ]

    def add_obstacle(self, obstacle: tuple[int, int]):
        self.obstacles.append(obstacle)

    def remove_obstacle(self, obstacle: tuple[int, int]):
        self.obstacles.remove(obstacle)

    def has_obstacle(self, obstacle: tuple[int, int]):
        return obstacle in self.obstacles
