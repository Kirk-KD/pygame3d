from collections import deque
import pygame as pg

from renderer.sprite_object import AnimatedSpriteObject
from config import *


class Weapon(AnimatedSpriteObject):
    def __init__(self, game, damage: int, max_ammo: int, init_ammo: int, sprite_sheet_dir: str, frame_time: float, scale: float, sound: pg.mixer.Sound) -> None:
        super().__init__(game, sprite_sheet_dir, animation_time=frame_time, scale=scale)
        self.images = deque([pg.transform.scale(img, (img.get_width() * self.sprite_scale, img.get_height() * self.sprite_scale))
                             for img in self.images])
        self.weapon_position = self.get_weapon_position(self.images[0])

        self.reloading: bool = False
        self.damage: int = damage
        self.max_ammo: int = max_ammo
        self.ammo: int = init_ammo
        self.num_images: int = len(self.images)
        self.frame_counter: int = 0

        self.sound: pg.mixer.Sound = sound
    
    def animate_shot(self) -> None:
        if self.reloading:
            self.game.player.weapon_shot = False
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
    
    def ammo_full(self) -> bool:
        return self.ammo == self.max_ammo
    
    def add_ammo(self, amount: int) -> None:
        self.ammo = min(self.ammo + amount, self.max_ammo)


class Pistol(Weapon):
    def __init__(self, game) -> None:
        super().__init__(game,
                         damage=35,
                         max_ammo=200,
                         init_ammo=50,
                         sprite_sheet_dir="weapons/pistol",
                         frame_time=90,
                         scale=3,
                         sound=game.audio_manager.pistol)


class Shotgun(Weapon):
    def __init__(self, game) -> None:
        super().__init__(game,
                         damage=50,
                         max_ammo=50,
                         init_ammo=8,
                         sprite_sheet_dir="weapons/shotgun",
                         frame_time=100,
                         scale=3,
                         sound=game.audio_manager.shotgun)
