from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from config import *


class Map:
    def __init__(self) -> None:
        self.map: list[list[str]] = []
        self.height: int = 0
        self.width: int = 0

        self.pathfind_grid: Grid = None
        self.pathfinder: AStarFinder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
    
    def load(self, map: list[list[str]]) -> None:
        """From the given 2D list representation of the map, load the pathfinding 2D list 
        in the format required by the pathfinding library.

        Args:
            map (list[list[str]]): The original 2D map with texture names representing 
                walls and space representing an empty cell.
        """
        self.map = map
        self.height = len(self.map)
        self.width = max(len(row) for row in self.map)
        
        grid = []
        for row in range(self.height):
            g_row = []
            for col in range(self.width):
                if col > len(self.map[row]) - 1:
                    g_row.append(1)
                else:
                    if self.map[row][col] == " ":
                        g_row.append(1)
                    else:
                        g_row.append(0)
            grid.append(g_row)
        self.pathfind_grid = Grid(matrix=grid)

    def unoccupied(self, x: int, y: int) -> bool:
        """Checks whether or not the cell at x,y is unoccupied.

        Args:
            x (int): The x (column) of the cell to check.
            y (int): The y (row) of the cell to check.

        Returns:
            bool: True if unoccupied, False otherwise.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            try:
                return self.map[y][x] == " "
            except IndexError:
                return True
        
        return True

    def astar_next(self, start: tuple[int, int], target: tuple[int, int]) -> tuple[int, int] or None:
        """Using the A* algorithm, find the next step to go to when pathfinding towards `target`.

        Args:
            start (tuple[int, int]): The starting position of the pathfinder, in grid units.
            target (tuple[int, int]): The target position to pathfind to, in grid units.

        Returns:
            tuple[int, int] or None: The next grid to go to, or None if the algorithm could not 
                find a valid path to `target` on the grid.
        """
        self.pathfind_grid.cleanup()

        n_start = self.pathfind_grid.node(*start)
        n_end = self.pathfind_grid.node(*target)

        path, runs = self.pathfinder.find_path(n_start, n_end, self.pathfind_grid)
        if len(path) <= 1:
            return None
        else:
            return path[1]
        # print('operations:', runs, 'path length:', len(path))
        # print(self.pathfind_grid.grid_str(path=path, start=n_start, end=n_end))
