from constants import *
from wall import VerticalWall
from camera import Camera
from geometry import Point3D, RotationXY
from util import distance

import pygame as pg
from math import radians

pg.init()

WIN = pg.display.set_mode(WIN_RES)
CLOCK = pg.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

cam = Camera(Point3D(0, 0, 0), RotationXY(0, 0))
walls = [
    VerticalWall(Point3D(-1, 1, 1), Point3D(1, -1, 1), cam, RED),
    VerticalWall(Point3D(-1, 1, -1), Point3D(-1, -1, 1), cam, GREEN),
    VerticalWall(Point3D(1, 1, 1), Point3D(1, -1, -1), cam, BLUE)
]

pg.event.set_grab(True)
pg.mouse.set_visible(False)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
        
        if event.type == pg.MOUSEMOTION:
            ox = event.rel[0]
            cam.orientation.rotateY(radians(-MOUSE_SENSITIVITY * ox))
    
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        cam.moveZ(MOVE_SPEED)
    if keys[pg.K_s]:
        cam.moveZ(-MOVE_SPEED)
    if keys[pg.K_a]:
        cam.moveX(-MOVE_SPEED)
    if keys[pg.K_d]:
        cam.moveX(MOVE_SPEED)
    if keys[pg.K_SPACE]:
        cam.orientation.set_zeros()
    if keys[pg.K_ESCAPE]:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
    
    WIN.fill(BLACK)

    lines_to_draw = set()
    for wall in walls:
        lines_to_draw.update(wall.lines_to_draw())
    
    for line_start, line_end, color in lines_to_draw:
        pg.draw.line(WIN, color, line_start, line_end)

    pg.display.update()
    CLOCK.tick(FPS)
