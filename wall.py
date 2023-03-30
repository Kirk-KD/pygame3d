import pygame as pg

from camera import Camera
from geometry import Point3D, transform_vertex, project_vertex
from constants import *
from util import clamp


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
        camera_matrix = self.camera.get_camera_matrix()
        vertices_cam = [transform_vertex(vertex.to_tuple(), camera_matrix) for vertex in self.vertices]
        vertices_proj = [project_vertex(vertex_cam, self.camera.projection_plane_distance) for vertex_cam in vertices_cam]

        vertices_proj.sort(key=lambda v: v[0])

        min_x = min(vertices_proj[0][0], vertices_proj[1][0])
        max_x = max(vertices_proj[2][0], vertices_proj[3][0])
        left_y = min(vertices_proj[0][1], vertices_proj[1][1])
        right_y = min(vertices_proj[2][1], vertices_proj[3][1])
        y_diff_per_x_pixel = (right_y - left_y) / (max_x - min_x)

        left_height = abs(vertices_proj[0][1] - vertices_proj[1][1])
        right_height = abs(vertices_proj[2][1] - vertices_proj[3][1])
        height_diff_per_x_pixel = (right_height - left_height) / (max_x - min_x)
        
        x = min_x - 1
        y = left_y
        height = left_height

        if x < -WIN_HALF:
            missing_x = -WIN_HALF - x
            x = -WIN_HALF
            y += y_diff_per_x_pixel * missing_x
            height += height_diff_per_x_pixel * missing_x
        
        if max_x > WIN_HALF:
            max_x = WIN_HALF - 1

        # print(vertices_proj)

        line_no = 0
        while x < max_x:
            x += 1
            y += y_diff_per_x_pixel
            height += height_diff_per_x_pixel

            line_start = clamp(WIN_HALF + x, 0, WIN_WIDTH), clamp(WIN_HALF - y, 0, WIN_HEIGHT)
            line_end = clamp(WIN_HALF + x, 0, WIN_WIDTH), clamp(WIN_HALF - (y + height), 0, WIN_HEIGHT)

            if line_no == 0:
                color = 255, 0, 0
            else:
                color = 255, 255, 255
            pg.draw.line(surface, color, line_start, line_end)

            line_no += 1
        # pg.draw.line(surface, (0, 255, 0), line_start, line_end)

