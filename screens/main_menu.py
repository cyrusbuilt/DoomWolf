import pygame as pg
import pygame_menu as pm
from typing import Optional

from screens import RGBColors


class MainMenu:

    def __init__(self, title: str, width: int = 700, height: int = 800):
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode((width, height))
        self.main_menu: pm.Menu = pm.Menu(title=title,
                                          width=width,
                                          height=height,
                                          theme=pm.themes.THEME_DARK)
        self.options_menu: Optional[pm.Menu] = None

    @property
    def width(self) -> int:
        return self.screen.get_width()

    @property
    def height(self) -> int:
        return self.screen.get_height()

    def close_menu(self):
        self.main_menu.disable()

    def set_options_menu(self, menu: pm.Menu):
        self.options_menu = menu

    def show_menu(self):
        pg.display.set_caption(self.main_menu.get_title())
        self.main_menu.get_theme().widget_alignment = pm.locals.ALIGN_CENTER
        self.main_menu.add.button(title="Start",
                                  action=self.close_menu,
                                  font_color=RGBColors.WHITE.value,
                                  background_color=RGBColors.RED.value)
        self.main_menu.add.label(title="")
        self.main_menu.add.button(title="Options",
                                  action=self.options_menu,
                                  font_color=RGBColors.WHITE.value,
                                  background_color=RGBColors.RED.value)
        self.main_menu.add.label(title="")
        self.main_menu.add.button(title="Exit",
                                  action=pm.events.EXIT,
                                  font_color=RGBColors.WHITE.value,
                                  background_color=RGBColors.RED.value)
        self.main_menu.mainloop(self.screen)
        pg.display.quit()
