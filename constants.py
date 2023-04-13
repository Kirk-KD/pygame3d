import math

WIN_HALF = 400
WIN_WIDTH, WIN_HEIGHT = WIN_RES = WIN_HALF * 2, WIN_HALF * 2
FOV = math.radians(90)
# FOV = 1 / math.tan(150 / 2)
FPS = 110

MOVE_SPEED = 3  # multiply this with deltatime
MOUSE_SENSITIVITY = 0.1

PLAYER_COLLIDER_RADIUS = 0.6

WALL_SIZE = 5

FOG_START = 25
SKY_COLOR = 66, 51, 0
WALL_COLOR = 219, 182, 57
FLOOR_COLOR = 94, 78, 23
