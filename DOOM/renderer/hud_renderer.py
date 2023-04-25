import pygame as pg
import random

from config import WIN_WIDTH, WIN_HEIGHT


class HUDRenderer:
    def __init__(self, game) -> None:
        self.game = game

        self.load_textures()
        self.face = self.face_80[0]

        self.face_frames = 0

    def update(self) -> None:
        # self.face = 

        self.face_frames += 1
        if self.face_frames >= 30:
            self.face_frames = 0
            self.face = random.choice(self.get_faces())

    def draw(self) -> None:
        self.game.surface.blit(self.main, (0, WIN_HEIGHT - self.main.get_height()))
        self.game.surface.blit(self.face, (0, 0))  # TODO
    
    def get_faces(self) -> list[pg.Surface]:
        health = self.game.player.health
        if health >= 80:
            return self.face_80
        elif health >= 60:
            return self.face_60
        elif health >= 40:
            return self.face_40
        elif health >= 20:
            return self.face_20
        elif health >= 1:
            return self.face_01
        else:
            return [self.face_death]

    def load_textures(self) -> None:
        self.main: pg.Surface = self.fit_width(self.load("main"))

        self.face_80 = [self.load("face/80_0"), self.load("face/80_1"), self.load("face/80_2")]
        self.face_60 = [self.load("face/60_0"), self.load("face/60_0"), self.load("face/60_0")]
        self.face_40 = [self.load("face/40_0"), self.load("face/40_0"), self.load("face/40_0")]
        self.face_20 = [self.load("face/20_0"), self.load("face/20_0"), self.load("face/20_0")]
        self.face_01 = [self.load("face/01_0"), self.load("face/01_0"), self.load("face/01_0")]
        self.face_death = self.load("face/0")
    
    def load(self, path: str) -> pg.Surface:
        return pg.image.load("DOOM/resources/textures/hud/" + path + ".png")

    def fit_width(self, surf: pg.Surface) -> pg.Surface:
        width, height = surf.get_size()
        ratio = WIN_WIDTH / width
        new_height = height * ratio
        return pg.transform.scale(surf, (WIN_WIDTH, new_height))
