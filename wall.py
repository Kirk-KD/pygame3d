import pygame as pg

from camera import Camera
from geometry import Point3D, transform_vertex, project_vertex
from constants import *


class TopDownPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = x, y


class HorizontalLine:
    def __init__(self, x: int, mid_y: int, height: int, color):
        self.x = x
        self.mid_y = mid_y
        self.height = height
        self.half_height = height / 2
        self.color = color
    
    def draw(self, surface: pg.Surface):
        pg.draw.line(surface, self.color, (self.x, self.mid_y - self.half_height), (self.x, self.mid_y + self.half_height))


class Wall2D:
    def __init__(self, start_point: TopDownPoint, end_point: TopDownPoint):
        self.start = start_point
        self.end = end_point


class Plane:
    def __init__(self, vertices: list[Point3D], camera: Camera):
        self.vertices = vertices
        self.camera = camera
    
    def draw(self, surface: pg.Surface):
        screen_width, screen_height = WIN_RES

        camera_matrix = self.camera.get_camera_matrix()
        vertices_cam = [transform_vertex(vertex.to_tuple(), camera_matrix) for vertex in self.vertices]
        vertices_proj = [project_vertex(vertex_cam, self.camera.projection_plane_distance) for vertex_cam in vertices_cam]



        for i in range(len(self.vertices)):
            x1, y1 = vertices_proj[i]
            x2, y2 = vertices_proj[(i + 1) % len(self.vertices)]
            pg.draw.line(surface, (255, 255, 255), (x1 + screen_width // 2, screen_height // 2 - y1), (x2 + screen_width // 2, screen_height // 2 - y2))

