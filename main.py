from constants import *
from wall import Plane
from camera import Camera
from geometry import Point3D, RotationXY

import pygame as pg
from math import radians

pg.init()

WIN = pg.display.set_mode(WIN_RES)

BLACK = 0, 0, 0
WHITE = 255, 255, 255

cam = Camera(Point3D(0, 0, 0), RotationXY(0, radians(20)))
p = Plane([Point3D(-1, 1, 2), Point3D(1, 1, 4), Point3D(1, -1, 4), Point3D(-1, -1, 2)], cam)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
    
    WIN.fill(BLACK)

    p.draw(WIN)
    cam.orientation.y += 0.001

    pg.display.update()
