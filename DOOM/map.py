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
        if 0 <= x < self.width and 0 <= y < self.height:
            try:
                return self.map[y][x] == " "
            except IndexError:
                return True
        
        return True

    def astar_next(self, start: tuple[int, int], target: tuple[int, int]) -> tuple[int, int] or None:
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
