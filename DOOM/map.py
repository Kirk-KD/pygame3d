from config import *


class Map:
    def __init__(self, path: str) -> None:
        self.map: list[list[int]] = self.load_map(path)
        self.height: int = len(self.map)
        self.width: int = len(self.map[0])

    def unoccupied(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x] == 0
        
        return True

    def load_map(self, path: str) -> list[list[int]]:
        result = [[]]
        with open(path, "r") as f:
            s = f.read()
            for c in s:
                if c == "\n":
                    result.append([])
                elif c == " ":
                    result[-1].append(0)
                else:
                    result[-1].append(int(c))
        return result
    
    def __str__(self) -> str:
        res = ""
        for row in self.map:
            for cell in row:
                res += str(cell) if cell else " "
            res += "\n"
        return res.strip()
