import pygame as pg

from config import *


class TextureData:
    def __init__(self, path: str, resolution: tuple = (TEX_SIZE, TEX_SIZE)):
        self.texture: pg.Surface = pg.transform.scale(pg.image.load(path).convert_alpha(), resolution)
        self.width, self.height = self.texture.get_size()


# WALL_TEX = TextureData("DOOM/textures/wall.png")
