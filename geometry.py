import numpy as np  # import numpy for advanced math
import math

from constants import WIN_HALF  # math for basic math


class Point3D:
    """
    Class representing a 3D point in the world space.
    """

    def __init__(self, x, y, z):
        # initialize the object
        self.x = x
        self.y = y
        self.z = z
    
    def to_tuple(self):
        """Return a tuple containing the x y z, to use with rendering math."""

        return self.x, self.y, self.z

    def copy(self):
        """Returns a copy of this object. Do not use too much, expensive on memory."""

        return Point3D(self.x, self.y, self.z)

    def __str__(self):
        """String representation of this object."""

        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"

    def __repr__(self):
        """General representation of this object (just a call to __str__)."""

        return self.__str__()


class RotationXY:
    """Object representing the rotation along the x (up and down) and y (left and right). All the values are in RADIANS."""

    def __init__(self, x, y):
        # initialize the object
        self.x = x
        self.y = y
    
    def rotateY(self, v):
        """Rotate along the y axis, and flip the signs if the rotation result is out of range [-PI, PI]."""

        self.y += v  # update the rotation first
        if self.y >= math.pi:  # out of range
            self.y = -math.pi + (self.y - math.pi)  # fix the value
        elif self.y < -math.pi:  # out of range
            self.y = math.pi - (self.y + math.pi)  # fix the value
    
    def set_zeros(self):
        """Set the rotations to zero, use for debug purposes."""

        self.x = 0
        self.y = 0
    
    def __str__(self):
        """String representation."""

        return f"RotationXY(x={self.x}, y={self.y})"


def transform_vertex(vertex, transform_matrix):
    """Transform the vertex (x, y, z) using np.concatenate and dot."""

    vertex_homog = np.concatenate((vertex, np.array([1])), axis=0)  # concatenate along the axis
    vertex_transformed = np.dot(transform_matrix, vertex_homog)
    return vertex_transformed[:3]  # x, y, z


def project_vertex(vertex, projection_plane_distance):
    """Project the vertex from world space to camera space, using the distance to the projection plane."""

    x, y, z = vertex
    if z <= 0:  # prevent division by zero
        z = 0.001

    # just math for calculating the projection
    x_proj = x * projection_plane_distance / z
    y_proj = y * projection_plane_distance / z

    print(x_proj)

    if x_proj > WIN_HALF:
        x_proj = WIN_HALF + (x_proj - WIN_HALF) * 0.1

    # return a numpy array of the x and y pixel position
    return np.array([x_proj, y_proj])
