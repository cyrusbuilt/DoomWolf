import math
import os

ASSETS_BASE = "assets"
SOUND_BASE = os.path.join(ASSETS_BASE, 'sound')
ENEMY_SOUND_BASE = os.path.join(SOUND_BASE, "enemy")
WEAPON_SOUND_BASE = os.path.join(SOUND_BASE, "weapon")
SPRITE_BASE = os.path.join(ASSETS_BASE, "sprites")
ANIM_SPRITE_BASE = os.path.join(SPRITE_BASE, "animated_sprites")
ENEMY_SPRITE_BASE = os.path.join(SPRITE_BASE, "enemy")
STATIC_SPRITE_BASE = os.path.join(SPRITE_BASE, "static")
WEAPON_SPRITE_BASE = os.path.join(SPRITE_BASE, "weapon")
TEXTURE_BASE = os.path.join(ASSETS_BASE, "textures")
WALL_TEXTURE_BASE = os.path.join(TEXTURE_BASE, "walls")
DIGITS_TEXTURE_BASE = os.path.join(TEXTURE_BASE, 'digits')
DATA_BASE = "data"
MAP_DATA_BASE = os.path.join(DATA_BASE, "maps")
ENEMY_DATA_BASE = os.path.join(DATA_BASE, "enemies")
WEAPON_DATA_BASE = os.path.join(DATA_BASE, "weapons")

DEBUG = False
GOD_MODE = False
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0

PLAYER_POS = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# Need to move this to map/level definition
FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH // math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
