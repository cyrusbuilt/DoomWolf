import json
import os
import pygame as pg
import pygame_menu as pm
from typing import Optional

from engine import constants as con
from engine import RGBColors
from game import util
from screens.load_game import LoadGameMenu


class PauseScreen:

    def __init__(self, game):
        self.game = game
        res_w: int = game.screen.get_width()
        res_h: int = game.screen.get_height()
        self.menu: pm.Menu = pm.Menu(title="Paused",
                                     width=res_w,
                                     height=res_h,
                                     theme=pm.themes.THEME_DARK)
        self.load_game_menu: Optional[LoadGameMenu] = None
        self.created: bool = False
        self.is_shown: bool = False

    def close_menu(self):
        # TODO Move this to input_handler?
        pg.mouse.set_visible(con.DEBUG)

        self.game.handle_pause()
        self.menu.disable()
        self.is_shown = False

    def save_game(self):
        door_data: list[dict] = []
        doors = self.game.object_handler.sprite_map.door_sprites
        for d in doors:
            door_data.append({
                "id": d.id,
                "name": d.name,
                "pos_x": d.x,
                "pos_y": d.y,
                "interactive": d.is_interactive,
                "removed": d.removed,
                "tile_count": d.tile_count,
                "previous_pos_x": d.previous_pos_x,
                "previous_pos_y": d.previous_pos_y
            })

        enemy_data: list[dict] = []
        enemies = self.game.object_handler.enemy_list
        for e in enemies:
            enemy_data.append({
                "id": e.id,
                "name": e.name,
                "pos_x": e.x,
                "pos_y": e.y,
                "alive": e.alive,
                "health": e.health,
                "removed": e.removed,
                "player_search_trigger": e.player_search_trigger,
                "ray_cast_value": e.ray_cast_value
            })

        item_data: list[dict] = []
        items = self.game.object_handler.sprite_map.item_sprites
        for i in items:
            item_data.append({
                "id": i.id,
                "name": i.name,
                "interactive": i.is_interactive,
                "pos_x": i.x,
                "pos_y": i.y,
                "removed": i.removed
            })

        save_data = {
            "map": self.game.map.name,
            "player": {
                "pos_x": self.game.player.x,
                "pos_y": self.game.player.y,
                "health": self.game.player.health,
                "armor": self.game.player.armor,
                "angle": self.game.player.angle,
                "rel": self.game.player.rel
            },
            "weapon": {
                "current": self.game.current_weapon.name,
                "total_ammo": self.game.current_weapon.total_ammo,
                "remaining_ammo": self.game.current_weapon.ammo_remaining
            },
            "doors": door_data,
            "enemies": enemy_data,
            "items": item_data
        }

        save_path = util.get_user_save_game_path()
        os.makedirs(save_path, exist_ok=True)
        save_file = os.path.join(save_path, f"{save_data['map']}.sav")
        base_name = os.path.splitext(save_file)[0]
        if os.path.exists(save_file):
            for i in range(50):
                new_file = f'{base_name}_{i}.sav'
                new_file_path = os.path.join(save_path, new_file)
                if not os.path.exists(new_file_path):
                    save_file = new_file_path
                    break

        with open(save_file, 'w') as file:
            json.dump(save_data, file, indent=2)
            file.write("\n")
        self.menu.add.label(
            title=f"Saved game: {os.path.splitext(save_file)[0]}")
        print(f'Saved game state to: {save_file}')

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
            self.menu.add.button(title="Save Game",
                                 action=self.save_game,
                                 font_color=RGBColors.WHITE.value,
                                 background_color=RGBColors.RED.value)
            self.menu.add.label("")
            if self.load_game_menu:
                self.menu.add.button(title="Load Game",
                                     action=self.load_game_menu.get_current(),
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

    def set_load_game_menu(self, menu: LoadGameMenu):
        self.load_game_menu = menu

    def get_current(self) -> pm.Menu:
        return self.menu
