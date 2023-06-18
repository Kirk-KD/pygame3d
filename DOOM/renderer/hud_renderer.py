import pygame as pg
import os
import random

from config import WIN_WIDTH, WIN_HEIGHT, WIN_HALF_WIDTH


class HUDText:
    def __init__(self) -> None:
        self.big_lookup: dict[str, pg.Surface] = self.load_textures("big")
        self.small_lookup: dict[str, pg.Surface] = self.load_textures("small")
    
    def string_to_surface(self, s: str, lookup_name: str, scale: float = 1, margin: float = 0) -> pg.Surface:
        surfaces = []
        for char in s.lower():
            if char == ".":
                char = "dot"
            elif char == ":":
                char = "colon"
            elif char == " ":
                char = "space"
            surf = getattr(self, lookup_name + "_lookup")[char]
            surfaces.append(surf)
        width = sum([surface.get_width() + margin for surface in surfaces])
        new_surface = pg.Surface((width, surfaces[0].get_height()), pg.SRCALPHA, 32).convert_alpha()
        x = 0
        for surface in surfaces:
            new_surface.blit(surface, (x, 0))
            x += surface.get_width() + margin
        
        return pg.transform.scale(new_surface, (new_surface.get_width() * scale, new_surface.get_height() * scale))
    
    def load_textures(self, size_name: str) -> dict[str, pg.Surface]:
        res = {}
        for filename in os.listdir(f"DOOM/resources/textures/hud/text/{size_name}"):
            name = filename.split(".")[0]
            res[name] = self.load(name, size_name)
        return res

    def load(self, name: str, size_name: str) -> pg.Surface:
        return pg.image.load(f"DOOM/resources/textures/hud/text/{size_name}/" + name + ".png")


class HUDRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.hud_text = HUDText()

        self.load_textures()

        self.face: pg.Surface = self.face_80[0]
        self.face_position: tuple[int, int] = None
        self.update_face_position()
        self.face_frames: int = 0

        scale = 3.5
        self.grey_numbers = [
            self.load("weapon_numbers/grey_2", scale=scale),
            self.load("weapon_numbers/grey_3", scale=scale),
            self.load("weapon_numbers/grey_4", scale=scale),
            self.load("weapon_numbers/grey_5", scale=scale),
            self.load("weapon_numbers/grey_6", scale=scale),
            self.load("weapon_numbers/grey_7", scale=scale)
        ]
        self.yellow_numbers = [
            self.load("weapon_numbers/yellow_2", scale=scale),
            self.load("weapon_numbers/yellow_3", scale=scale),
            self.load("weapon_numbers/yellow_4", scale=scale),
            self.load("weapon_numbers/yellow_5", scale=scale),
            self.load("weapon_numbers/yellow_6", scale=scale),
            self.load("weapon_numbers/yellow_7", scale=scale)
        ]

        self.console_text: str = None
        self.console_frames: int = 0
        self.console_max_frames: int = 0

        self.health_position: tuple[int, int] = 282, WIN_HEIGHT - 75
        self.ammo_position: tuple[int, int] = 85, WIN_HEIGHT - 75
        self.armor_position: tuple[int, int] = 772, WIN_HEIGHT - 75
        self.console_position: tuple[int, int] = 10, 10

    def update(self) -> None:
        self.face_frames += 1
        if self.face_frames >= 30:
            self.face_frames = 0
            self.face = random.choice(self.get_faces())
        
        if self.console_text:
            self.console_frames += 1
            if self.console_frames >= self.console_max_frames:
                self.console_text = None
                self.console_frames = 0
                self.console_max_frames = 0
    
    def console(self, text: str, frames: int) -> None:
        self.console_text = text
        self.console_max_frames = frames

    def draw(self) -> None:
        self.game.surface.blit(self.main, (0, WIN_HEIGHT - self.main.get_height()))
        self.game.surface.blit(self.face, self.face_position)

        health_surf = self.hud_text.string_to_surface(str(self.game.player.health) + "%", "big", scale=2.7)
        self.game.surface.blit(health_surf, self.centered(health_surf, self.health_position))

        ammo_surf = self.hud_text.string_to_surface(str(self.game.player.weapon.ammo), "big", scale=2.7)
        self.game.surface.blit(ammo_surf, self.centered(ammo_surf, self.ammo_position))

        armor_surf = self.hud_text.string_to_surface(str(self.game.player.armor) + "%", "big", scale=2.7)
        self.game.surface.blit(armor_surf, self.centered(armor_surf, self.armor_position))

        self.draw_console_text()
        self.draw_weapon_numbers()
    
    def draw_console_text(self) -> None:
        if self.console_text:
            console_surf = self.hud_text.string_to_surface(self.console_text, "small", scale=3, margin=0)
            self.game.surface.blit(console_surf, self.console_position)
    
    def draw_weapon_numbers(self) -> None:
        top_left = 415, WIN_HEIGHT - 105
        x_diff = 45
        y_diff = 37

        x, y = top_left
        for i in range(6):
            self.game.surface.blit((self.yellow_numbers if self.game.player.inventory.has_weapon_at(i) else self.grey_numbers)[i], (x, y))

            x += x_diff
            if i == 2:
                y += y_diff
                x = top_left[0]
    
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
    
    def load(self, path: str, scale: float = 1) -> pg.Surface:
        img = pg.image.load("DOOM/resources/textures/hud/" + path + ".png")
        if scale == 1:
            return img
        return pg.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    
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
    
    def centered(self, surf: pg.Surface, center: tuple[int, int]) -> tuple[int, int]:
        x, y = center
        return x - surf.get_width() // 2, y - surf.get_height() // 2
