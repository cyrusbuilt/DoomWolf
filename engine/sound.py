import os
import pygame as pg
from typing import Optional

from engine import constants as con


class Sound:

    def __init__(self):
        pg.mixer.pre_init(buffer=4096, channels=16)
        pg.mixer.init()
        self.path: str = con.SOUND_BASE
        self.music_loaded: bool = False
        self.music_path: str = os.path.join(self.path, 'theme.mp3')
        self.item_channel: pg.mixer.Channel = pg.mixer.Channel(
            con.AUDIO_ITEM_CHANNEL)
        self.body_channel: pg.mixer.Channel = pg.mixer.Channel(
            con.AUDIO_BODY_CHANNEL)
        self.fadeout_interval: int = con.AUDIO_FADE_OUT

        self.player_pain: Optional[pg.mixer.Sound] = None
        player_pain_path = os.path.join(self.path, 'player_pain.wav')
        if os.path.exists(player_pain_path):
            print(f'Loading player pain sound: {player_pain_path}')
            self.player_pain = pg.mixer.Sound(player_pain_path)

        self.player_movement: Optional[pg.mixer.Sound] = None
        player_movement_path = os.path.join(self.path, 'footstep.wav')
        if os.path.exists(player_movement_path):
            print(f'Loading player movement sound: {player_movement_path}')
            self.player_movement = pg.mixer.Sound(player_movement_path)

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

    @staticmethod
    def get_sprite_sounds(sprite_name: str) -> dict[str, pg.mixer.Sound]:
        print(f"Loading sounds for sprite '{sprite_name}' ...")
        path = os.path.join(con.DOOR_SOUND_BASE, sprite_name)
        if not os.path.isdir(path):
            path = os.path.join(con.ITEM_SOUND_BASE, sprite_name)
        return Sound._load_sounds_for_path(path)

    def load_game_music(self):
        if os.path.exists(self.music_path):
            print(f'Loading theme music: {self.music_path}')
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.set_volume(0.4)
            self.music_loaded = True

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

    def fadeout(self):
        pg.mixer.fadeout(self.fadeout_interval)

    @staticmethod
    def play_sound(sound: pg.mixer.Sound):
        pg.mixer.find_channel(True).play(sound)
