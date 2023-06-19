from PIL import Image
from typing import Tuple

from player import Player

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

    (0, 0, 17): "SW1STARG",

    (0, 0, 18): "STONE2",
    (0, 0, 19): "STONE3",
    (0, 0, 20): "STONGARG",

    (0, 0, 21): "MARBLE3",

    (0, 0, 22): "SP_DUDE1",
    (0, 0, 23): "SP_DUDE2",
    (0, 0, 24): "MARBFAC2",
    (0, 0, 25): "MARBFAC3",
    (0, 0, 26): "SKULWAL3",
    (0, 0, 27): "MARBFACE",
    (0, 0, 28): "MARBLOD1"
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

                    if RGB_TO_TEX[rgb] == "SW1STARG":  # lever
                        self.next_level = x, y
            map.append(row)

        return map
    
    def get(self, x: int, y: int) -> Tuple[int, int, int]:
        return self.pixels[x, y]

    def can_use_lever(self, player: Player):
        pgx, pgy = player.grid_position
        nlx, nly = self.next_level
        return abs(pgx - nlx) <= 1 and abs(pgy - nly) <= 1
