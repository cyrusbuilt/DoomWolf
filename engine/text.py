import os
import pygame as pg

from engine import constants as con
from engine import RGBColors


class Text:

    def __init__(self, game, pos: tuple[float, float], string: str,
                 color: RGBColors, font_name: str, size: int):
        self.game = game
        self.pos: tuple[float, float] = pos
        self.string: str = string
        self.color: RGBColors = color
        self.size: int = size
        font_path = os.path.join(con.FONT_BASE, font_name)
        self.font: pg.font.Font = pg.font.Font(font_path, self.size)
        self.layout: pg.Surface = self.font.render(self.string, True,
                                                   self.color.value)

    def draw(self):
        self.game.screen.blit(self.layout, self.pos)

    def update_text(self, string: str):
        self.string = string
        self.layout = self.font.render(self.string, True, self.color.value)

    def update_pos(self, pos: tuple[float, float]):
        self.pos = pos
