import math

WIN_WIDTH: int = 1600
WIN_HALF_WIDTH: int = WIN_WIDTH // 2
WIN_HEIGHT: int = 900
WIN_HALF_HEIGHT: int = WIN_HEIGHT // 2
# ASPECT_RATIO: float = 1  # square window

FPS: int = 60

FOV: float = math.radians(80)
HALF_FOV: float = FOV / 2
RAYS: float = WIN_WIDTH // 2
HALF_RAYS: float = RAYS // 2
DELTA_ANGLE: float = FOV / RAYS
MAX_DEPTH = 20
SCREEN_DISTANCE: float = WIN_HALF_WIDTH / math.tan(HALF_FOV)
SCALE: int = WIN_WIDTH // RAYS

PLAYER_ROT_SPEED: float = math.radians(120)
PLAYER_MOVE_SPEED: float = 3.5
PLAYER_SIZE_SCALE: float = 0.03

ENEMY_SIZE_SCALE: float = 0.3

MOUSE_SPEED: float = 0.0025
MOUSE_MAX_REL: float = 40
MOUSE_BORDER_LEFT: float = 100
MOUSE_BORDER_RIGHT: float = WIN_WIDTH - MOUSE_BORDER_LEFT

GRID_SIZE: float = 1

TEX_SIZE: int = 256
HALF_TEX_SIZE: int = TEX_SIZE // 2
