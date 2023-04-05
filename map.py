import random  # ramdom library
from dataclasses import dataclass  # data class decorator

from constants import WALL_SIZE, WALL_COLOR  # wall size and color from constants.py
from wall import VerticalWall  # object representing a wall
from geometry import Point3D  # object representing a 3D point
from camera import Camera  # the Camera object from camera.py

# short names for convenience
T = True
F = False


@dataclass
class MapCell:
    """
    A Dataclass representing a cell in the randomly generated map.
    """

    row: int
    col: int
    top_wall: bool
    right_wall: bool
    bottom_wall: bool
    left_wall: bool
    
    @property
    def all_walls(self):
        """Property that returns the booleans representing the existences of all the walls."""
        return (self.top_wall, self.right_wall, self.bottom_wall, self.left_wall)


class Map:
    """
    Object that handles the generation of the map, and converts it to VerticalWall objects.
    """

    def __init__(self, width: int, height: int, start_row: int, start_col: int, random_holes: int, camera: Camera):
        # 2D list of cells
        self.map = None

        # initialize the size of the map
        self.width = width
        self.height = height

        # initialize the row and column indice to start maze generation
        self.start_row = start_row
        self.start_col = start_col

        # how many cells should be randomly set to empty
        self.random_holes = random_holes

        # stores the camera
        self.camera = camera

        # start generation
        self.generate()
    
    def generate(self):
        """Generate the map using Randomized Prim's algorithm (https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm)."""

        # initialize the map with empty cells
        self.map = [[MapCell(r, c, T, T, T, T) for c in range(self.width)] for r in range(self.height)]
        
        # stack representation
        stack = [self.map[self.start_row][self.start_col]]

        # keep track of all the visited cells
        visited = [self.map[self.start_row][self.start_col]]

        # while the stack is not empty (while the maze is not done being generated)
        while stack:
            # pop the top cell from the stack and store it as the current cell
            cell = stack.pop()

            # get all the neightbours of the cell
            neightbours = []
            if cell.row != 0:
                neightbours.append(self.map[cell.row - 1][cell.col])
            if cell.row != self.height - 1:
                neightbours.append(self.map[cell.row + 1][cell.col])
            if cell.col != 0:
                neightbours.append(self.map[cell.row][cell.col - 1])
            if cell.col != self.width - 1:
                neightbours.append(self.map[cell.row][cell.col + 1])

            # make sure to delete the neighbours that have been visited
            neightbours = list(filter(lambda x: x not in visited, neightbours))
            
            # if there are any unvisited neighbours
            if neightbours:
                # add the previously popped cell back to the stack
                stack.append(cell)

                # select a random neighbour
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
                
                # mark the random neighbour as visited
                visited.append(rand_nei)
                # and put it on top of the stack
                stack.append(rand_nei)
        
        # set random cells empty by:
        for cell in random.choices([
            c for c in sum(self.map, [])  # flatten the 2D list into a 1D list using sum()
                if any(c.all_walls)  # if the cell has any walls
                and c.row != 0  # and it is not on any of the sides
                and c.row != self.height - 1
                and c.col != 0
                and c.col != self.width - 1
        ], k=self.random_holes):  # select "self.random_holes" amount of cells from all qualified cells
            # remove all the walls
            cell.top_wall = F
            cell.bottom_wall = F
            cell.left_wall = F
            cell.right_wall = F
    
    def to_walls(self):
        """Convert the map to VerticalWall objects."""

        # initialize the set of walls (use set for better performance).
        walls = set()

        # loop through all rows...
        for row in range(self.height):
            # loop through all columns (all cells):
            for col in range(self.width):
                # select the cell
                cell = self.map[row][col]
                
                # if the cell has a top on top, add a top wall
                if cell.top_wall:
                    walls.add(
                        VerticalWall(
                            Point3D(col * WALL_SIZE, WALL_SIZE, row * WALL_SIZE),
                            Point3D((col + 1) * WALL_SIZE, 0, row * WALL_SIZE),
                            self.camera, WALL_COLOR
                        )
                    )
                # etc
                if cell.left_wall:
                    walls.add(
                        VerticalWall(
                            Point3D(col * WALL_SIZE, WALL_SIZE, (row + 1) * WALL_SIZE),
                            Point3D(col * WALL_SIZE, 0, row * WALL_SIZE),
                            self.camera, WALL_COLOR
                        )
                    )
        
        # add a line of walls for the missing right border of the map
        for row in range(self.height):
            walls.add(  # add a wall to walls
                VerticalWall(  # create a wall
                    Point3D(self.width * WALL_SIZE, WALL_SIZE, row * WALL_SIZE),
                    Point3D(self.width * WALL_SIZE, 0, (row + 1) * WALL_SIZE),
                    self.camera, WALL_COLOR
                )
            )
        
        # add a line of walls for the missing bottom border of the map
        for col in range(self.width):
            walls.add(  # add a wall to walls
                VerticalWall(  # create a wall
                    Point3D(col * WALL_SIZE, WALL_SIZE, self.height * WALL_SIZE),
                    Point3D((col + 1) * WALL_SIZE, 0, self.height * WALL_SIZE),
                    self.camera, WALL_COLOR
                )
            )
        
        # finally return the created list of walls
        return walls

    def __str__(self):
        """
        Function that returns a string display of the map when this object is passed to the str() function.
        """
        
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

