import os
import pygame as pg

from engine import constants as con
from engine import RGBColors
from engine.text import Text


class Hud:

    def __init__(self, game):
        self.game = game
        image_path = os.path.join(con.STATIC_SPRITE_BASE, "hud.png")
        sprite = pg.image.load(image_path).convert()
        w = self.game.screen.get_width()
        h = self.game.screen.get_height()
        win_h = h * 0.08
        self.sprite: pg.Surface = pg.transform.scale(sprite, (w, win_h))
        self.rect: pg.Rect = self.sprite.get_rect()
        self.rect.topleft = (0, h - win_h)
        text_y = self.rect.y + int(self.rect.height / 2.5)
        text_x = int(self.rect.width / 35)
        self.armor_text: Text = Text(game, (text_x, text_y), 'ARMOR',
                                     RGBColors.DARK_GRAY, 'DUGAFONT.ttf', 35)
        text_x = int(self.rect.width / 3.4)
        self.health_text: Text = Text(game, (text_x, text_y), 'HEALTH',
                                      RGBColors.DARK_GRAY, 'DUGAFONT.ttf', 35)
        text_x = int(self.rect.width / 1.8)
        self.ammo_text: Text = Text(game, (text_x, text_y), 'AMMO',
                                    RGBColors.DARK_GRAY, 'DUGAFONT.ttf', 35)
        text_x = self.rect.width / 1.2
        self.wpn_text: Text = Text(game, (text_x, text_y), 'WEAPON',
                                   RGBColors.DARK_GRAY, 'DUGAFONT.ttf', 35)
        self.all_text: list[Text] = [self.armor_text, self.health_text,
                                     self.ammo_text, self.wpn_text]

    def update(self):
        self.game.screen.blit(self.sprite, self.rect)
        p_armor = self.game.player.armor
        p_health = self.game.player.health
        tot_ammo = self.game.current_weapon.total_ammo
        rem_ammo = self.game.current_weapon.ammo_remaining
        wpn_name = self.game.current_weapon.name

        self.armor_text.update_text(f'{p_armor} / {con.PLAYER_MAX_ARMOR}')
        self.health_text.update_text(f'{p_health} / {con.PLAYER_MAX_HEALTH}')
        self.ammo_text.update_text(f'{rem_ammo} / {tot_ammo}')
        self.wpn_text.update_text(wpn_name)

        for text in self.all_text:
            text.draw()
