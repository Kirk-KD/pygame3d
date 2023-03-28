import numpy as np
import math

from geometry import Point3D, RotationXY
from constants import FOV, WIN_WIDTH


class Camera:
    def __init__(self, position: Point3D, orientation: RotationXY):
        self.position = position
        self.orientation = orientation
        self.projection_plane_distance = 0.5 * (WIN_WIDTH / math.tan(FOV / 2))
    
    def get_camera_matrix(self):
        # Compute the rotation matrix for the camera orientation
        Rx = np.array([[1, 0, 0],
                    [0, np.cos(self.orientation.x), -np.sin(self.orientation.x)],
                    [0, np.sin(self.orientation.x), np.cos(self.orientation.x)]])
        Ry = np.array([[np.cos(self.orientation.y), 0, np.sin(self.orientation.y)],
                    [0, 1, 0],
                    [-np.sin(self.orientation.y), 0, np.cos(self.orientation.y)]])
        R = np.dot(Ry, Rx)

        # Compute the translation matrix for the camera position
        t = np.array(self.position.to_tuple()).reshape((3, 1))

        # Combine the rotation and translation matrices to get the camera matrix
        camera_matrix = np.concatenate((R, -np.dot(R, t)), axis=1)
        camera_matrix = np.concatenate((camera_matrix, np.array([[0, 0, 0, 1]])), axis=0)

        return camera_matrix
