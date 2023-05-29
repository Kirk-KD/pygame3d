from PIL import Image
from typing import Tuple

RGB_TO_TEX = {
    (0, 0, 0): "STARTAN3",
    (255, 0, 0): "STARG3",
    (0, 255, 0): "COMPTILE",
    (0, 0, 255): "COMPOHSO",
    (255, 255, 0): "BROWN1",
    (255, 0, 255): "BROWN96",
    (0, 255, 255): "SKIN2",
    (0, 0, 1): "COMPSTA1",
    (0, 0, 2): "COMPSTA2",
    (0, 0, 3): "STARTAN2",
    (0, 0, 4): "COMPUTE1",
    (0, 0, 5): "STARBR2",
    (0, 0, 6): "COMPUTE3",

    (0, 0, 7): "CEMENT3",
    (0, 0, 8): "CEMENT1",
    (0, 0, 9): "CEMENT2",
    (0, 0, 10): "CEMENT4",
    (0, 0, 11): "CEMENT5",
    (0, 0, 12): "CEMENT6",
    (0, 0, 13): "CEMPOIS",

    (0, 0, 14): "LITEMET",
    (0, 0, 15): "MARBFAC2",
    (0, 0, 16): "MARBFAC3",

    (0, 0, 17): "SW1STARG"
}


class PNGMap:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.image: Image = Image.open(self.path)
        self.pixels = self.image.load()

    def to_map(self) -> None:
        map = []
        for y in range(self.image.height):
            row = []
            for x in range(self.image.width):
                r, g, b, a = self.get(x, y)
                rgb = r, g, b
                if rgb == (255, 255, 255):
                    row.append(" ")
                else:
                    row.append(RGB_TO_TEX[rgb])
            map.append(row)
        # print("\n".join(["".join(row) for row in map]))
        return map
    
    def get(self, x: int, y: int) -> Tuple[int, int, int]:
        return self.pixels[x, y]
