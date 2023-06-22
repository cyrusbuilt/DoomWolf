import os
import pygame as pg
from typing import Optional

from engine import constants as con


class Sound:

    def __init__(self):
        pg.mixer.init()
        self.path: str = con.SOUND_BASE
        self.music_loaded: bool = False
        self.auto_channel: pg.mixer.Channel = pg.mixer.Channel(0)

        # TODO make loading theme music more dynamic (like weapon sounds)
        # so that they can be loaded with the levels/maps
        self.music_path: str = os.path.join(self.path, 'theme.mp3')
        if os.path.exists(self.music_path):
            print(f'Loading theme music: {self.music_path}')
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.set_volume(0.4)
            self.music_loaded = True

        self.player_pain: Optional[pg.mixer.Sound] = None
        player_pain_path = os.path.join(self.path, 'player_pain.wav')
        if os.path.exists(player_pain_path):
            print(f'Loading player pain sound: {player_pain_path}')
            self.player_pain = pg.mixer.Sound(player_pain_path)

        self.enemy_pain: Optional[pg.mixer.Sound] = None
        enemy_pain_path = os.path.join(self.path, 'npc_pain.wav')
        if os.path.exists(enemy_pain_path):
            print(f'Loading enemy pain sound: {enemy_pain_path}')
            self.enemy_pain = pg.mixer.Sound(enemy_pain_path)

        self.enemy_death: Optional[pg.mixer.Sound] = None
        enemy_death_path = os.path.join(self.path, 'npc_death.wav')
        if os.path.exists(enemy_death_path):
            print(f'Loading enemy death sound: {enemy_death_path}')
            self.enemy_death = pg.mixer.Sound(enemy_death_path)

        self.enemy_attack: Optional[pg.mixer.Sound] = None
        enemy_attack_path = os.path.join(self.path, 'npc_attack.wav')
        if os.path.exists(enemy_attack_path):
            print(f'Loading enemy attack sound: {enemy_attack_path}')
            self.enemy_attack = pg.mixer.Sound(enemy_attack_path)
            self.enemy_attack.set_volume(0.2)

    @property
    def music_playing(self) -> bool:
        return pg.mixer.music.get_busy()

    @staticmethod
    def _load_sounds_for_path(path: str) -> dict[str, pg.mixer.Sound]:
        sounds: dict[str, pg.mixer.Sound] = {}
        for file_name in os.listdir(path):
            ext = os.path.splitext(file_name)[1]
            if ext == '.wav' or ext == '.ogg':
                full_path = os.path.join(path, file_name)
                sounds[file_name] = pg.mixer.Sound(full_path)
        return sounds

    @staticmethod
    def get_weapon_sounds(weapon_name: str) -> dict[str, pg.mixer.Sound]:
        print(f"Loading sounds for weapon '{weapon_name}'...")
        path = os.path.join(con.WEAPON_SOUND_BASE, weapon_name)
        return Sound._load_sounds_for_path(path)

    @staticmethod
    def get_enemy_sounds(enemy_name: str) -> dict[str, pg.mixer.Sound]:
        print(f"Loading sounds for enemy '{enemy_name}'...")
        path = os.path.join(con.ENEMY_SOUND_BASE, enemy_name)
        return Sound._load_sounds_for_path(path)

    def play_music(self):
        if self.music_loaded:
            pg.mixer.music.play(-1)
        else:
            print(f"ERROR: Can't play music. Not loaded.")

    def pause_music(self):
        if self.music_loaded and self.music_playing:
            pg.mixer.music.pause()

    def resume_music(self):
        if self.music_loaded and not self.music_playing:
            pg.mixer.music.unpause()

    def set_music_volume(self, volume: float):
        if self.music_loaded:
            pg.mixer.music.set_volume(volume)
