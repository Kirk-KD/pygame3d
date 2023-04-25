from collections import deque
import pygame as pg

from renderer.sprite_object import AnimatedSpriteObject
from config import *


class Weapon(AnimatedSpriteObject):
    def __init__(self, game, damage: int, sprite_sheet_dir: str, frame_time: float, scale: float, sound: pg.mixer.Sound) -> None:
        super().__init__(game, sprite_sheet_dir, animation_time=frame_time, scale=scale)
        self.images = deque([pg.transform.scale(img, (img.get_width() * self.sprite_scale, img.get_height() * self.sprite_scale))
                             for img in self.images])
        self.weapon_position = self.get_weapon_position(self.images[0])

        self.reloading: bool = False
        self.damage: int = damage
        self.num_images: int = len(self.images)
        self.frame_counter: int = 0

        self.sound: pg.mixer.Sound = sound
    
    def animate_shot(self) -> None:
        if self.reloading:
            self.player.weapon_shot = False
            if self.anim_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.weapon_position = self.get_weapon_position(self.image)
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
    
    def get_weapon_position(self, img) -> tuple:
        return (WIN_HALF_WIDTH - img.get_width() // 2, WIN_HEIGHT - img.get_height() - self.game.hud_renderer.main.get_height())
    
    def draw(self) -> None:
        self.game.surface.blit(self.images[0], self.weapon_position)
    
    def play_sound(self) -> None:
        self.game.audio_manager.play(self.sound)
    
    def update(self) -> None:
        self.check_anim_time()
        self.animate_shot()


class Shotgun(Weapon):
    def __init__(self, game) -> None:
        super().__init__(game, 50, "weapons/shotgun", 100, 3, game.audio_manager.shotgun)


class Pistol(Weapon):
    def __init__(self, game) -> None:
        super().__init__(game, 30, "weapons/pistol", 90, 3, game.audio_manager.pistol)
