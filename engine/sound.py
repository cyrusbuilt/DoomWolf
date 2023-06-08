import os
import pygame as pg
from typing import Optional


class Sound:

    def __init__(self):
        pg.mixer.init()
        self.path: str = 'assets/sound'
        self.music_loaded: bool = False
        self.music_playing: bool = False
        self.music_path: str = os.path.join(self.path, 'theme.mp3')
        if os.path.exists(self.music_path):
            print(f'Loading theme music: {self.music_path}')
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.set_volume(0.4)
            self.music_loaded = True

        self.shotgun: Optional[pg.mixer.Sound] = None
        shotgun_path = os.path.join(self.path, 'shotgun.wav')
        if os.path.exists(shotgun_path):
            print(f'Loading weapon sound: {shotgun_path}')
            self.shotgun = pg.mixer.Sound(shotgun_path)

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

    def play_music(self):
        if self.music_loaded:
            pg.mixer.music.play(-1)
            self.music_playing = True
        else:
            print(f"ERROR: Can't play music. Not loaded.")

    def pause_music(self):
        if self.music_loaded and self.music_playing:
            pg.mixer.music.pause()
            self.music_playing = False

    def resume_music(self):
        if self.music_loaded and not self.music_playing:
            pg.mixer.music.unpause()
            self.music_playing = True
