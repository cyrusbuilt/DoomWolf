import sys

import pygame as pg
from typing import Optional

from engine import constants as con
from engine.hud import Hud
from engine.input_handler import InputEvent
from engine.input_handler import InputHandler
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
        self.input: InputHandler = InputHandler(self)
        self.screen: pg.Surface = pg.display.set_mode(con.RES)
        self.window_title: str = ''
        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: int = 1
        self.global_trigger: bool = False
        self.paused: bool = False
        self.global_event: int = pg.USEREVENT + 0
        self.map: Optional[Map] = None
        self.sound: Sound = Sound()
        self.player: Player = Player(self)
        self.ray_caster: Optional[RayCaster] = None
        self.object_renderer: ObjectRenderer = ObjectRenderer(self)
        self.current_weapon: Optional[Weapon] = None
        self.object_handler: ObjectHandler = ObjectHandler(self)
        self.path_finder: Optional[PathFinder] = None
        pg.time.set_timer(self.global_event, 40)
        self.hud: Hud = Hud(self)

    def new_game(self, skip_default_map_load: bool = False):
        if not skip_default_map_load:
            self.map = Map(self, 'level1')
            self.map.load_map()

        self.input.setup()

        self.sound.load_game_music()

        self.player.reset()

        self.object_renderer.setup()

        self.ray_caster = RayCaster(self)

        self.object_handler.setup()
        self.object_handler.spawn_entities()

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
        self.hud.update()
        self.delta_time = self.clock.tick(con.FPS)
        title = self.window_title
        # if con.DEBUG:
        title += f' FPS: {self.clock.get_fps() :.1f}'

        pg.display.set_caption(title)
        pg.display.flip()

    def draw(self):
        if con.DEBUG:
            self.screen.fill('black')
            self.map.draw()
            self.player.draw()
        else:
            self.object_renderer.draw()
            self.current_weapon.draw()

    def handle_pause(self):
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

    def do_events(self, events: set[InputEvent]):
        pass

    def check_events(self):
        self.global_trigger = False

        events = self.input.get_input_events()
        for event in events:
            if event == InputEvent.SCREENSHOT:
                self._handle_screenshot()
            elif event == InputEvent.PAUSE:
                self.handle_pause()
            elif event == InputEvent.TOGGLE_FULLSCREEN:
                pg.display.toggle_fullscreen()
            elif event == InputEvent.INTERACT:
                self.player.interact = True
            elif event == InputEvent.QUIT:
                pg.quit()
                sys.exit()
            elif event == InputEvent.GLOBAL_EVENT:
                self.global_trigger = True

        if not self.paused:
            self.player.single_fire_event(events)

        self.do_events(events)

    def run(self):
        while True:
            self.check_events()
            if not self.paused:
                self.update()
                self.draw()
