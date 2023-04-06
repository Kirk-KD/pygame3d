import pygame as pg

WALL = pg.image.load("wall.png")
WALL_WIDTH_PIXELS, WALL_HEIGHT_PIXELS = WALL.get_size()
WALL_STRIPS = []
for x in range(WALL_WIDTH_PIXELS):
    strip_rect = pg.Rect(x, 0, 1, WALL_HEIGHT_PIXELS)
    strip = WALL.subsurface(strip_rect)
    WALL_STRIPS.append(strip)
