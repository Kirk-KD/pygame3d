import random

from constants import WALL_SIZE, WALL_COLOR
from wall import VerticalWall
from geometry import Point3D
from camera import Camera

T = True
F = False


class MapCell:
    def __init__(self, row: int, col: int, top_wall: bool=False, right_wall: bool=False, bottom_wall: bool=False, left_wall: bool=False):
        self.row = row
        self.col = col

        self.top_wall = top_wall
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        self.left_wall = left_wall
    
    @property
    def all_walls(self):
        return (self.top_wall, self.right_wall, self.bottom_wall, self.left_wall)

    @property
    def is_empty(self):
        return not any(self.all_walls)


class Map:
    def __init__(self, width: int, height: int, start_row: int, start_col: int, random_holes: int, camera: Camera):
        self.width = width
        self.height = height
        self.start_row = start_row
        self.start_col = start_col
        self.random_holes = random_holes

        self.camera = camera

        self.generate()
    
    def generate(self):
        self.map = [[MapCell(r, c, T, T, T, T) for c in range(self.width)] for r in range(self.height)]
        
        stack = [self.map[self.start_row][self.start_col]]
        visited = [self.map[self.start_row][self.start_col]]

        while stack:
            cell = stack.pop()
            neightbours = []
            if cell.row != 0:
                neightbours.append(self.map[cell.row - 1][cell.col])
            if cell.row != self.height - 1:
                neightbours.append(self.map[cell.row + 1][cell.col])
            if cell.col != 0:
                neightbours.append(self.map[cell.row][cell.col - 1])
            if cell.col != self.width - 1:
                neightbours.append(self.map[cell.row][cell.col + 1])
            neightbours = list(filter(lambda x: x not in visited, neightbours))
            
            if neightbours:
                stack.append(cell)
                rand_nei = random.choice(neightbours)

                # delete connected walls
                if rand_nei.row > cell.row:
                    cell.bottom_wall = False
                    rand_nei.top_wall = False
                elif rand_nei.row < cell.row:
                    cell.top_wall = False
                    rand_nei.bottom_wall = False
                elif rand_nei.col > cell.col:
                    cell.right_wall = False
                    rand_nei.left_wall = False
                elif rand_nei.col < cell.col:
                    cell.left_wall = False
                    rand_nei.right_wall = False
                
                visited.append(rand_nei)
                stack.append(rand_nei)
        
        for cell in random.choices([c for c in sum(self.map, []) if any(c.all_walls) and c.row != 0 and c.row != self.height - 1 and c.col != 0 and c.col != self.width - 1], k=self.random_holes):
            cell.top_wall = F
            cell.bottom_wall = F
            cell.left_wall = F
            cell.right_wall = F
    
    def to_walls(self):
        walls = set()

        for row in range(self.height):
            for col in range(self.width):
                cell = self.map[row][col]
                
                if cell.top_wall:
                    walls.add(
                        VerticalWall(
                            Point3D(col * WALL_SIZE, WALL_SIZE, row * WALL_SIZE),
                            Point3D((col + 1) * WALL_SIZE, 0, row * WALL_SIZE),
                            self.camera, WALL_COLOR
                        )
                    )
                if cell.left_wall:
                    walls.add(
                        VerticalWall(
                            Point3D(col * WALL_SIZE, WALL_SIZE, (row + 1) * WALL_SIZE),
                            Point3D(col * WALL_SIZE, 0, row * WALL_SIZE),
                            self.camera, WALL_COLOR
                        )
                    )
        
        for row in range(self.height):
            walls.add(
                VerticalWall(
                    Point3D(self.width * WALL_SIZE, WALL_SIZE, row * WALL_SIZE),
                    Point3D(self.width * WALL_SIZE, 0, (row + 1) * WALL_SIZE),
                    self.camera, WALL_COLOR
                )
            )
        
        for col in range(self.width):
            walls.add(
                VerticalWall(
                    Point3D(col * WALL_SIZE, WALL_SIZE, self.height * WALL_SIZE),
                    Point3D((col + 1) * WALL_SIZE, 0, self.height * WALL_SIZE),
                    self.camera, WALL_COLOR
                )
            )
        
        return walls

    def __str__(self):
        result = ""
        for row in self.map:
            result += "█"
            for cell in row:
                if cell.top_wall:
                    result += "██"
                else:
                    result += " █"
            result += "\n█"
            for cell in row:
                result += " "
                if cell.right_wall:
                    result += "█"
                else:
                    result += " "
            result += "\n"
        result += "█" + "██" * self.width
        return result

