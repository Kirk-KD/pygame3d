import pygame as pg
import os
import random

from config import WIN_WIDTH, WIN_HEIGHT, WIN_HALF_WIDTH


class HUDText:
    def __init__(self) -> None:
        self.lookup: dict[str, pg.Surface] = self.load_textures()
    
    def string_to_surface(self, s: str, scale: float = 1) -> pg.Surface:
        surfaces = []
        for char in s:
            surf = self.lookup[char]
            surfaces.append(surf)
        width = sum([surface.get_width() for surface in surfaces])
        new_surface = pg.Surface((width, surfaces[0].get_height()), pg.SRCALPHA, 32).convert_alpha()
        x = 0
        for surface in surfaces:
            new_surface.blit(surface, (x, 0))
            x += surface.get_width()
        
        return pg.transform.scale(new_surface, (new_surface.get_width() * scale, new_surface.get_height() * scale))
    
    def load_textures(self) -> dict[str, pg.Surface]:
        res = {}
        for filename in os.listdir("DOOM/resources/textures/hud/text/"):
            name = filename.split(".")[0]
            res[name] = self.load(name)
        return res

    def load(self, name: str) -> pg.Surface:
        return pg.image.load("DOOM/resources/textures/hud/text/" + name + ".png")


class HUDRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.hud_text = HUDText()

        self.load_textures()

        self.face: pg.Surface = self.face_80[0]
        self.face_position: tuple[int, int] = None
        self.update_face_position()
        self.face_frames: int = 0

        self.health_position: tuple[int, int] = 220, WIN_HEIGHT - 100

    def update(self) -> None:
        self.face_frames += 1
        if self.face_frames >= 30:
            self.face_frames = 0
            self.face = random.choice(self.get_faces())

    def draw(self) -> None:
        self.game.surface.blit(self.main, (0, WIN_HEIGHT - self.main.get_height()))
        self.game.surface.blit(self.face, self.face_position)
        print(self.game.player.health)
        self.game.surface.blit(self.hud_text.string_to_surface(str(self.game.player.health) + "%", scale=2.7), self.health_position)
    
    def update_face_position(self) -> None:
        self.face_position = WIN_HALF_WIDTH - self.face.get_width() // 2 + 1, WIN_HEIGHT - self.main.get_height() // 2 - self.face.get_height() // 2 + 1

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
            return self.face_death

    def load_textures(self) -> None:
        self.main: pg.Surface = self.fit_width(self.load("main"))

        self.face_80: list[pg.Surface] = self.load_faces("80")
        self.face_60: list[pg.Surface] = self.load_faces("60")
        self.face_40: list[pg.Surface] = self.load_faces("40")
        self.face_20: list[pg.Surface] = self.load_faces("20")
        self.face_01: list[pg.Surface] = self.load_faces("01")
        self.face_death: list[pg.Surface] = self.load_faces("0")
    
    def load(self, path: str) -> pg.Surface:
        return pg.image.load("DOOM/resources/textures/hud/" + path + ".png")
    
    def load_faces(self, health: str) -> list[pg.Surface]:
        face_ratio = 3.3
        faces = [self.load(f"face/{health}_{i}") for i in range(3)] if health != "0" else [self.load("face/0")]
        faces = [pg.transform.scale(face, (face.get_width() * face_ratio, face.get_height() * face_ratio)) for face in faces]
        return faces

    def fit_width(self, surf: pg.Surface) -> pg.Surface:
        width, height = surf.get_size()
        ratio = WIN_WIDTH / width
        new_height = height * ratio
        return pg.transform.scale(surf, (WIN_WIDTH, new_height))
