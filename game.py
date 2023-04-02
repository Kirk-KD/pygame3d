from math import radians
import pygame as pg
from camera import Camera

from constants import *
from geometry import Point3D, RotationXY
from map import Map
from util import clamp


class Game:
    def __init__(self, title: str, map_width: int, map_height: int, map_holes: int):
        self.title = title

        self.map_width = map_width
        self.map_height = map_height
        self.map_holes = map_holes

        self.running = False
        self.dt = None

    def __pre_init(self):
        pg.init()

        self.surface = pg.display.set_mode(WIN_RES)
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

    def __init(self):
        self.camera = Camera(Point3D(WALL_SIZE / 2, 1.5, WALL_SIZE / 2), RotationXY(0, 0))
        self.map = Map(self.map_width, self.map_height, 0, 0, self.map_holes, self.camera)
        self.walls = self.map.to_walls()
        self.camera.walls = self.walls
    
    def run(self):
        self.__pre_init()
        self.__init()

        self.running = True
        while self.running:
            self.__frame()
    
    def __frame(self):
        self.dt = self.__tick_delta()

        self.__poll_events()
        self.__keyboard_input()

        self.camera.move()
        
        self.__draw_sky()
        self.__draw_floor()
        self.__draw_walls()

        pg.display.update()
    
    def __tick_delta(self):
        return self.clock.tick(FPS) / 1000

    def __poll_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return
            
            if event.type == pg.MOUSEMOTION:
                self.camera.orientation.rotateY(radians(-MOUSE_SENSITIVITY * event.rel[0]))
    
    def __keyboard_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.camera.pre_move_z(MOVE_SPEED * self.dt)
        if keys[pg.K_s]:
            self.camera.pre_move_z(-MOVE_SPEED * self.dt)
        if keys[pg.K_a]:
            self.camera.pre_move_x(-MOVE_SPEED * self.dt)
        if keys[pg.K_d]:
            self.camera.pre_move_x(MOVE_SPEED * self.dt)
        if keys[pg.K_SPACE]:
            self.camera.orientation.set_zeros()
        if keys[pg.K_ESCAPE]:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
    
    def __draw_walls(self):
        lines_to_draw = set()
        for wall in self.walls:
            lines_to_draw.update(wall.lines_to_draw())
        
        # columns = [None] * (WIN_WIDTH + 1)
        for line in sorted(lines_to_draw, key=lambda l: l.dist_to_cam, reverse=True):
            if line.dist_to_cam > FOG_START:
                continue

            # columns[int(line.line_start[0])] = line.draw(WIN, columns[int(line.line_start[0])])
            line.draw(self.surface)
    
    def __draw_sky(self):
        self.surface.fill(SKY_COLOR)
    
    def __draw_floor(self):
        for y in range(WIN_HALF):
            r = clamp((1 - (WIN_HALF - y) / WIN_HALF), 0, 1)
            cr, cg, cb = FLOOR_COLOR
            color = int(cr * r), int(cg * r), int(cb * r)
            pg.draw.line(self.surface, color, (0, WIN_HALF + y), (WIN_WIDTH, WIN_HALF + y))
