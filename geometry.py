import numpy as np
import math


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
    if z <= 0:
        z = 0.001
    x_proj = x * projection_plane_distance / z
    # print(f"x_proj = {x} * {projection_plane_distance} / {z} = {x_proj}")
    y_proj = y * projection_plane_distance / z
    return np.array([x_proj, y_proj])
