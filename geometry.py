import numpy as np
import math

from constants import WIN_WIDTH, WIN_HEIGHT


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self):
        return self.x, self.y, self.z

    def __str__(self):
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

    def __repr__(self):
        return self.__str__()


class RotationXY:
    """XY rotation, in radians."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def rotateY(self, v):
        self.y += v
        if self.y >= math.pi:
            self.y = -math.pi + (self.y - math.pi)
        elif self.y < -math.pi:
            self.y = math.pi - (self.y + math.pi)
    
    def set_zeros(self):
        self.x = 0
        self.y = 0
    
    def __str__(self):
        return f"RotationXY(x={self.x}, y={self.y})"


def transform_vertex(vertex, transform_matrix):
    vertex_homog = np.concatenate((vertex, np.array([1])), axis=0)
    vertex_transformed = np.dot(transform_matrix, vertex_homog)
    return vertex_transformed[:3]

def project_vertex(vertex, projection_plane_distance):
    x, y, z = vertex
    x_proj = x * projection_plane_distance / z
    print(f"x_proj = {x} * {projection_plane_distance} / {z} = {x_proj}")
    y_proj = y * projection_plane_distance / z
    return np.array([x_proj, y_proj])

# def project_vertex(vertex, projection_plane_distance):
#     x, y, z = vertex
#     if z <= 0:
#         # If the vertex is behind the camera, project it on the edge of the screen
#         x_proj = x * projection_plane_distance / max(0.0001, -z)
#         y_proj = y * projection_plane_distance / max(0.0001, -z)
#         # Clamp x_proj and y_proj to the screen edges
#         x_proj = min(max(x_proj, -WIN_WIDTH / 2), WIN_WIDTH / 2)
#         y_proj = min(max(y_proj, -WIN_HEIGHT / 2), WIN_HEIGHT / 2)
#     else:
#         # If the vertex is in front of the camera, project it normally
#         x_proj = x * projection_plane_distance / z
#         y_proj = y * projection_plane_distance / z

    # return np.array([x_proj, y_proj])


def limit_projection(target, reference):
    x1, y1 = target
    x2, y2 = reference

    m = (y1 - y2) / (x1 - x2)
    b = y1 - m * x1

    if x1 <= -WIN_WIDTH:
        new_x = -WIN_WIDTH
        new_y = m * (-WIN_WIDTH ) + b
    elif x1 >= WIN_WIDTH:
        new_x = WIN_WIDTH
        new_y = m * WIN_WIDTH + b
    else:
        return x1, y1

    return new_x, new_y
