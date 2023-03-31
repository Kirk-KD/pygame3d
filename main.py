from constants import *
from wall import Plane
from camera import Camera
from geometry import Point3D, RotationXY

import pygame as pg
from math import radians

pg.init()

WIN = pg.display.set_mode(WIN_RES)
CLOCK = pg.time.Clock()

BLACK = 0, 0, 0
WHITE = 255, 255, 255

cam = Camera(Point3D(0, 0, 0), RotationXY(0, 0))
p = Plane([Point3D(-1, 1, 2), Point3D(1, 1, 2), Point3D(1, -1, 2), Point3D(-1, -1, 2)], cam)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
    
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        cam.orientation.rotateY(radians(0.5))
    elif keys[pg.K_RIGHT]:
        cam.orientation.rotateY(radians(-0.5))
    elif keys[pg.K_SPACE]:
        cam.orientation.set_zeros()
    
    WIN.fill(BLACK)

    p.draw(WIN)

    pg.display.update()
    CLOCK.tick(FPS)
