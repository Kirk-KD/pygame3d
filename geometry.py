import numpy as np


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self):
        return self.x, self.y, self.z


class RotationXY:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def transform_vertex(vertex, transform_matrix):
    vertex_homog = np.concatenate((vertex, np.array([1])), axis=0)
    vertex_transformed = np.dot(transform_matrix, vertex_homog)
    return vertex_transformed[:3]


def project_vertex(vertex, projection_plane_distance):
    x, y, z = vertex
    x_proj = x * projection_plane_distance / z
    y_proj = y * projection_plane_distance / z
    return np.array([x_proj, y_proj])
