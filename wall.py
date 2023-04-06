import pygame as pg
import numpy as np

from camera import Camera
from geometry import Point3D, transform_vertex, project_vertex
from constants import *
from util import clamp, distance
from textures import WALL_STRIPS


class VerticalLine:
    def __init__(self, line_start: tuple, line_end: tuple, color: tuple, dist_to_cam: float, strip_idx: int):
        self.line_start = line_start
        self.line_end = line_end
        self.dist_to_cam = dist_to_cam
        try:
            self.texture = WALL_STRIPS[strip_idx]
        except:
            print(strip_idx, len(WALL_STRIPS))
            raise KeyError

        r = 1 - clamp(dist_to_cam / FOG_START, 0, 1)
        cr, cg, cb = color
        self.color = int(cr * r), int(cg * r), int(cb * r)
    
    def draw(self, surf: pg.Surface):
        # pg.draw.line(surf, self.color, self.line_start, self.line_end)
        surf.blit(self.texture, self.line_start)
    
    # def draw2(self, surf: pg.Surface, skip_over_y = None):
    #     if skip_over_y is None:
    #         pg.draw.line(surf, self.color, self.line_start, self.line_end)
    #         return (self.line_start[1], self.line_end[1])

    #     skip_end_y, skip_start_y = skip_over_y
    #     x, y1 = self.line_start
    #     y2 = self.line_end[1]

    #     if y1 < skip_start_y:
    #         if y2 < skip_start_y:
    #             pg.draw.line(surf, self.color, (x, y1), (x, y2))
    #             return (y1, skip_end_y)
    #         elif y2 <= skip_end_y:
    #             pg.draw.line(surf, self.color, (x, y1), (x, skip_start_y - 1))
    #             return (y1, skip_end_y)
    #         else:
    #             pg.draw.line(surf, self.color, (x, y1), (x, skip_start_y - 1))
    #             pg.draw.line(surf, self.color, (x, y2), (x, skip_end_y + 1))
    #             return y1, y2
    #     elif y1 <= skip_end_y:
    #         if y2 <= skip_end_y:
    #             return skip_over_y
    #         else:
    #             pg.draw.line(surf, self.color, (x, skip_end_y + 1), (x, y2))
    #             return (skip_start_y, y2)
    #     else:
    #         pg.draw.line(surf, self.color, self.line_start, self.line_end)
    #         return skip_over_y


class Plane:
    def __init__(self, vertices: list[Point3D], camera: Camera, color: tuple[3]):
        self.vertices = vertices
        self.camera = camera
        self.color = color

    def lines_to_draw(self):
        lines = set()

        camera_matrix = self.camera.get_camera_matrix()
        vertices_cam = [transform_vertex(vertex.to_tuple(), camera_matrix) for vertex in self.vertices]
        if not any([z > 0 for x, y, z in vertices_cam]):
            return set()
        vertices_proj = [np.append(project_vertex(vertex_cam, self.camera.projection_plane_distance), vertex_cam[2]) for vertex_cam in vertices_cam]
        vertices_proj.sort(key=lambda v: v[0])

        min_x = min(vertices_proj[0][0], vertices_proj[1][0])
        max_x = max(vertices_proj[2][0], vertices_proj[3][0])
        left_y = min(vertices_proj[0][1], vertices_proj[1][1])
        right_y = min(vertices_proj[2][1], vertices_proj[3][1])
        left_z = vertices_proj[0][2]
        right_z = vertices_proj[3][2]
        y_diff_per_x_pixel = (right_y - left_y) / (max_x - min_x)
        z_diff_per_x_pixel = (right_z - left_z) / (max_x - min_x)

        left_height = abs(vertices_proj[0][1] - vertices_proj[1][1])
        right_height = abs(vertices_proj[2][1] - vertices_proj[3][1])
        height_diff_per_x_pixel = (right_height - left_height) / (max_x - min_x)
        
        x = min_x
        y = left_y
        z = left_z
        height = left_height

        if x < -WIN_HALF:
            missing_x = -WIN_HALF - x
            x = -WIN_HALF
            y += y_diff_per_x_pixel * missing_x
            height += height_diff_per_x_pixel * missing_x

        if max_x > WIN_HALF:
            max_x = WIN_HALF - 1

        while x < max_x:
            x += 1
            y += y_diff_per_x_pixel
            z += z_diff_per_x_pixel
            height += height_diff_per_x_pixel

            if z_diff_per_x_pixel >= 0 and z > FOG_START:
                break
            if z_diff_per_x_pixel < 0 and z > FOG_START:
                continue

            line_start = clamp(WIN_HALF + x, 0, WIN_WIDTH), clamp(WIN_HALF - y, 0, WIN_HEIGHT)
            line_end = clamp(WIN_HALF + x, 0, WIN_WIDTH), clamp(WIN_HALF - (y + height), 0, WIN_HEIGHT)
            lines.add(VerticalLine(line_start, line_end, self.color, z, int(x - min_x) - 1))
        
        return lines
    
    def __str__(self):
        return f"Plane({self.vertices})"

    def __repr__(self):
        return self.__str__()

class VerticalWall(Plane):
    def __init__(self, top_left: Point3D, bottom_right: Point3D, camera: Camera, color: tuple[3]):
        self.top_left = top_left
        self.top_right = Point3D(bottom_right.x, top_left.y, bottom_right.z)
        self.bottom_left = Point3D(top_left.x, bottom_right.y, top_left.z)
        self.bottom_right = bottom_right
        super().__init__([self.top_left, self.top_right, self.bottom_right, self.bottom_left], camera, color)
