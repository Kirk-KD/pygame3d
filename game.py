from math import radians  # convert from degrees to radians
import pygame as pg  # pygame
from camera import Camera  # camera

from constants import *  # everything from constants.py
from geometry import Point3D, RotationXY  # 3D point and rotation
from map import Map  # map generator
from util import clamp  # clamp function


class Game:
    """The object representing the game."""

    def __init__(self, title: str, map_width: int, map_height: int, map_holes: int):
        # title of the game window
        self.title = title

        # map config
        self.map_width = map_width
        self.map_height = map_height
        self.map_holes = map_holes

        # flag for if the game is running or not
        self.running = False

        # deltatime to keep movement constance even under different FPS.
        self.dt = None

    def __pre_init(self):
        """Private function, initializes pygame and the window, and other small things."""

        pg.init()  # initialize pygame

        self.surface = pg.display.set_mode(WIN_RES)  # create the main window
        pg.display.set_caption(self.title)  # set title
        self.clock = pg.time.Clock()  # create the clock

        pg.event.set_grab(True)  # lock cursor
        pg.mouse.set_visible(False)  # hide cursor

    def __init(self):
        """Private function, initializes objects for the actual game itself."""

        # setup the camera
        self.camera = Camera(Point3D(WALL_SIZE / 2, 1.5, WALL_SIZE / 2), RotationXY(0, 0))

        # generate the map using the map setting in pre-init
        self.map = Map(self.map_width, self.map_height, 0, 0, self.map_holes, self.camera)

        # get the walls from the map
        self.walls = self.map.to_walls()

        # pass the walls to the camera
        self.camera.walls = self.walls
    
    def run(self):
        """The only public function, calls pre-init and init and runs the game."""

        self.__pre_init()
        self.__init()

        self.running = True  # set the flag to true
        while self.running:  # when the game is running
            self.__frame()  # call the frame
    
    def __frame(self):
        """Private function representing the operations in one frame."""

        # FPS tick and get the deltatime
        self.dt = self.__tick_delta()

        # get the events
        self.__poll_events()

        # get keyboard input
        self.__keyboard_input()

        # move the camera by the keyboard results
        self.camera.move()
        
        # draw the sky, aka background color
        self.__draw_sky()
        # draw the ground
        self.__draw_floor()
        # lastly draw the walls
        self.__draw_walls()

        # update the displace
        pg.display.update()
    
    def __tick_delta(self):
        """tick by the FPS and returns the deltatime"""

        return self.clock.tick(FPS) / 1000

    def __poll_events(self):
        """Check for pygame events."""

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
