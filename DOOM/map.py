from config import *


class Map:
    def __init__(self) -> None:
        self.map: list[list[str]] = []
        self.height: int = 0
        self.width: int = 0
    
    def load(self, map: list[list[str]]) -> None:
        self.map = map
        self.height = len(self.map)
        self.width = len(self.map[0])

    def unoccupied(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            try:
                return self.map[y][x] == " "
            except IndexError:
                return True
        
        return True
    
    def __str__(self) -> str:
        res = ""
        for row in self.map:
            for cell in row:
                res += str(cell) if cell else " "
            res += "\n"
        return res.strip()
