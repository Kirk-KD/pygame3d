import numpy as np
import math

from geometry import Point3D, RotationXY
from constants import FOV, WIN_WIDTH, PLAYER_COLLIDER_RADIUS
from util import distance


class Camera:
    def __init__(self, position: Point3D, orientation: RotationXY):
        self.position = position
        self.orientation = orientation
        self.projection_plane_distance = WIN_WIDTH / (2 * math.tan(FOV / 2))
        self.walls = None

        self.next_position = None
    
    def pre_move_x(self, v: float):
        if not self.next_position:
            self.next_position = self.position.copy()

        dx = v * math.cos(self.orientation.y)
        dz = v * math.sin(self.orientation.y)
        self.next_position.x += dx
        self.next_position.z += dz

    def pre_move_z(self, v: float):
        if not self.next_position:
            self.next_position = self.position.copy()

        dx = v * math.sin(self.orientation.y)
        dz = v * math.cos(self.orientation.y)
        self.next_position.x -= dx
        self.next_position.z += dz
    
    def pre_colision(self):
        if not self.next_position:
            return False

        for wall in self.walls:
            length = math.sqrt((wall.bottom_left.x - wall.bottom_right.x) ** 2 + (wall.bottom_left.z - wall.bottom_right.z) ** 2)
            dot_product = (self.next_position.x - wall.bottom_left.x) * (wall.bottom_right.x - wall.bottom_left.x) + (self.next_position.z - wall.bottom_left.z) * (wall.bottom_right.z - wall.bottom_left.z)

            if dot_product < 0 or dot_product > length ** 2:
                continue
            
            projection = dot_product / length ** 2
            closest_x = wall.bottom_left.x + projection * (wall.bottom_right.x - wall.bottom_left.x)
            closest_z = wall.bottom_left.z + projection * (wall.bottom_right.z - wall.bottom_left.z)
            distance = math.sqrt(((self.next_position.x - closest_x) ** 2 + (self.next_position.z - closest_z) ** 2))

            if distance <= PLAYER_COLLIDER_RADIUS:
                return True
        
        return False

    def move(self):
        if (not self.next_position) or self.pre_colision():
            self.next_position = None
            return
        
        self.position = self.next_position.copy()
    
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
