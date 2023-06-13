import sys

import pygame as pg
from typing import Optional

from engine import constants as con
from engine.map import Map
from engine.object_handler import ObjectHandler
from engine.object_renderer import ObjectRenderer
from engine.path_finder import PathFinder
from engine.player import Player
from engine.raycaster import RayCaster
from engine.sound import Sound
from engine.weapon import Weapon


class Game:

    def __init__(self):
        pg.init()
        joysticks = [
            pg.joystick.Joystick(x)
            for x in range(pg.joystick.get_count())
        ]
        self.joystick = joysticks[0]
        print(f'Joystick: {self.joystick.get_name()}')
        pg.mouse.set_visible(con.DEBUG)
        self.screen: pg.Surface = pg.display.set_mode(con.RES)
        pg.event.set_grab(True)
        self.window_title: str = ''
        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: int = 1
        self.global_trigger: bool = False
        self.paused: bool = False
        self.global_event: int = pg.USEREVENT + 0
        self.mouse_sensitivity: float = con.MOUSE_SENSITIVITY
        self.map: Optional[Map] = None
        self.player: Optional[Player] = None
        self.ray_caster: Optional[RayCaster] = None
        self.object_renderer: Optional[ObjectRenderer] = None
        self.current_weapon: Optional[Weapon] = None
        self.object_handler: Optional[ObjectHandler] = ObjectHandler(self)
        self.path_finder: Optional[PathFinder] = None
        self.sound: Optional[Sound] = None
        pg.time.set_timer(self.global_event, 40)
        # TODO Need a class for handling power-ups and inventory.
        # TODO Maybe support things like shield and extra health, etc.

    def new_game(self):
        # TODO Need to be able to load more than one map
        self.map = Map(self, 'level1')
        self.map.load_map()

        self.sound = Sound()

        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_caster = RayCaster(self)

        self.object_handler.spawn_sprites()
        self.object_handler.spawn_enemies()

        self.current_weapon = Weapon(self, '')

        self.path_finder = PathFinder(self)
        self.sound.play_music()

    def update(self):
        if self.paused:
            return

        self.player.update()
        self.ray_caster.update()
        self.object_handler.update()
        self.current_weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(con.FPS)
        title = self.window_title
        # if con.DEBUG:
        title += f' FPS: {self.clock.get_fps() :.1f}'

        pg.display.set_caption(title)

    def draw(self):
        if con.DEBUG:
            self.screen.fill('black')
            self.map.draw()
            self.player.draw()
        else:
            self.object_renderer.draw()
            self.current_weapon.draw()

    def _handle_pause(self):
        self.paused = not self.paused
        if self.paused:
            print('Game paused!')
            self.sound.pause_music()
            return

        print('Resuming game!')
        self.sound.resume_music()

    def _handle_screenshot(self):
        pg.image.save(self.screen, 'screenshot.jpg')
        print('Screenshot saved.')

    def do_event(self, event: pg.event.Event):
        pass

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            escaping = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self._handle_screenshot()
                elif event.key == pg.K_p:
                    self._handle_pause()
                elif event.key == pg.K_t:
                    pg.display.toggle_fullscreen()
                elif event.key == pg.K_ESCAPE:
                    escaping = True
            elif event.type == pg.JOYBUTTONDOWN:
                # TODO Probably should store controller ID and and button
                # mapping in a config file. Maybe also do the same for
                # for key map. This is all hard-coded for now, but should
                # make this user-configurable at some point.
                if event.button == 6:
                    self._handle_pause()
                elif event.button == 4:
                    escaping = True

            if event.type == pg.QUIT or escaping:
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True

            if not self.paused:
                self.player.single_fire_event(event)
                self.do_event(event)

    def run(self):
        while True:
            self.check_events()
            if not self.paused:
                self.update()
                self.draw()
