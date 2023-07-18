import pygame as pg
import pygame_menu as pm

from engine import constants as con
from screens import RGBColors


class PauseScreen:

    def __init__(self, game):
        self.game = game
        res_w: int = game.screen.get_width()
        res_h: int = game.screen.get_height()
        self.menu: pm.Menu = pm.Menu(title="Paused",
                                     width=res_w,
                                     height=res_h,
                                     theme=pm.themes.THEME_DARK)
        self.created: bool = False
        self.is_shown: bool = False

    def close_menu(self):
        # TODO Move this to input_handler?
        pg.mouse.set_visible(con.DEBUG)

        self.game.handle_pause()
        self.menu.disable()
        self.is_shown = False

    def event_loop(self):
        if self.menu.is_enabled():
            self.menu.mainloop(self.game.screen)

    def show_menu(self):
        if not self.created:
            self.menu.get_theme().widget_alignment = pm.locals.ALIGN_CENTER
            self.menu.add.button(title="Resume",
                                 action=self.close_menu,
                                 font_color=RGBColors.WHITE.value,
                                 background_color=RGBColors.RED.value)
            self.menu.add.label("")
            self.menu.add.button(title="Exit",
                                 action=pm.events.EXIT,
                                 font_color=RGBColors.WHITE.value,
                                 background_color=RGBColors.RED.value)
            self.created = True
        self.menu.enable()
        self.is_shown = True
