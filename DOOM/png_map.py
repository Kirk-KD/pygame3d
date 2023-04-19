from PIL import Image

RGB_TO_TEX = {
    (0, 0, 0): "STARTAN3",
    (255, 0, 0): "STARG3",
    (0, 255, 0): "COMPTILE",
    (0, 0, 255): "COMPOHSO",
    (255, 255, 0): "BROWN1",
    (255, 0, 255): "BROWN96"
}


class PNGMap:
    def __init__(self, path: str) -> None:
        self.path = path
        self.image = Image.open(self.path)
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
    
    def get(self, x: int, y: int) -> tuple[int, int, int]:
        return self.pixels[x, y]
