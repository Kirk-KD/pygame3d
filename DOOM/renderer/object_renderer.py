import pygame as pg
import os

from config import *
from renderer.texture import TextureData


class ObjectRenderer:
    """All renderings done here."""

    WALL_TEXTURES_KEYS = []

    def __init__(self, game) -> None:
        self.game = game
        self.surface: pg.Surface = game.surface
        self.wall_textures: dict[int, TextureData] = self.load_wall_textures()
        ObjectRenderer.WALL_TEXTURES_KEYS = list(self.wall_textures.keys())
        self.sky_texture: TextureData = self.load_sky_texture()
        self.sky_offset: float = 0
    
    def draw(self) -> None:
        self.render_sky()
        self.render_ground()
        self.render_objects()
    
    def render_objects(self) -> None:
        objs = sorted(self.game.raycast.objs_to_render, reverse=True, key=lambda o: o[0])
        for depth, image, pos in objs:
            self.surface.blit(image, pos)

    def render_sky(self) -> None:
        self.sky_offset = (self.sky_offset + 4 * self.game.player.mouse_rel) % WIN_WIDTH
        self.surface.blit(self.sky_texture.texture, (-self.sky_offset, 0))
        self.surface.blit(self.sky_texture.texture, (-self.sky_offset + WIN_WIDTH, 0))
    
    def render_ground(self) -> None:
        pg.draw.rect(self.surface, (30, 30, 30), (0, WIN_HALF_HEIGHT, WIN_WIDTH, WIN_HEIGHT))

    def load_wall_textures(self) -> dict[int, TextureData]:
        walls = {}
        base = "DOOM/resources/textures/walls/"
        for path in os.listdir(base):
            walls[path.split(".")[0]] = TextureData(base + path)
        return walls

    def load_sky_texture(self) -> TextureData:
        return TextureData("DOOM/resources/textures/skies/0.png", (WIN_WIDTH, WIN_HALF_HEIGHT))
