from constants import *
from util import clamp
from wall import VerticalWall
from camera import Camera
from geometry import Point3D, RotationXY
from map import Map

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

cam = Camera(Point3D(WALL_SIZE / 2, 1.5, WALL_SIZE / 2), RotationXY(0, 0))
maze_map = Map(7, 7, 0, 0, 5, cam)
walls = maze_map.to_walls()
cam.walls = walls

pg.event.set_grab(True)
pg.mouse.set_visible(False)

running = True
while running:
    dt = CLOCK.tick(FPS) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
        
        if event.type == pg.MOUSEMOTION:
            cam.orientation.rotateY(radians(-MOUSE_SENSITIVITY * event.rel[0]))
    
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        cam.pre_move_z(MOVE_SPEED * dt)
    if keys[pg.K_s]:
        cam.pre_move_z(-MOVE_SPEED * dt)
    if keys[pg.K_a]:
        cam.pre_move_x(-MOVE_SPEED * dt)
    if keys[pg.K_d]:
        cam.pre_move_x(MOVE_SPEED * dt)
    if keys[pg.K_SPACE]:
        cam.orientation.set_zeros()
    if keys[pg.K_ESCAPE]:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    cam.move()
    
    # sky
    WIN.fill(SKY_COLOR)

    # ground
    for y in range(WIN_HALF):
        r = clamp((1 - (WIN_HALF - y) / WIN_HALF), 0, 1)
        cr, cg, cb = FLOOR_COLOR
        color = int(cr * r), int(cg * r), int(cb * r)
        pg.draw.line(WIN, color, (0, WIN_HALF + y), (WIN_WIDTH, WIN_HALF + y))

    # walls
    lines_to_draw = set()
    for wall in walls:
        lines_to_draw.update(wall.lines_to_draw())
    
    # columns = [None] * (WIN_WIDTH + 1)
    for line in sorted(lines_to_draw, key=lambda l: l.dist_to_cam, reverse=True):
        if line.dist_to_cam > FOG_START:
            continue

        # columns[int(line.line_start[0])] = line.draw(WIN, columns[int(line.line_start[0])])
        line.draw(WIN)

    pg.display.update()
