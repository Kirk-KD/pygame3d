import pygame as pg
import os
from collections import deque

from config import *


class SpriteObject:
    def __init__(self, game, image_name: str, position: tuple[float, float] = (0, 0), scale: float = 1, shift: float = 0) -> None:
        self.game = game
        self.player = self.game.player
        self.x, self.y = position
        self.image: pg.Surface = pg.image.load("DOOM/resources/textures/sprites/" + image_name + ".png").convert_alpha()
        self.image_width, self.image_height = self.image.get_size()
        self.image_half_width, self.image_half_height = self.image_width // 2, self.image_height // 2
        self.image_ratio = self.image_width / self.image_height

        self.sprite_scale = scale
        self.sprite_height_shift = shift

        self.dx, self.dy = 0, 0
        self.theta = 0
        self.screen_x = 0
        self.dist = 1
        self.norm_dist = 1
        self.sprite_half_width = 0

    def get_sprite_projection(self) -> None:
        proj = SCREEN_DISTANCE / self.norm_dist * self.sprite_scale
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        h_shift = proj_height * self.sprite_height_shift
        pos = self.screen_x - self.sprite_half_width, WIN_HALF_HEIGHT - proj_height // 2 + h_shift

        self.game.raycast.objs_to_render.append((self.norm_dist, image, pos))
    
    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.image_half_width < self.screen_x < (WIN_WIDTH + self.image_half_width) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self) -> None:
        self.get_sprite()


class AnimatedSpriteObject(SpriteObject):
    def __init__(self, game, sprite_sheet_dir: str, animation_time: float, position: tuple[float, float] = (0, 0), scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, sprite_sheet_dir + "/0", position, scale, shift)
        
        self.animation_time = animation_time
        self.path = "DOOM/resources/textures/sprites/" + sprite_sheet_dir
        self.images = self.get_images(self.path)

        self.anim_time_prev: float = pg.time.get_ticks()
        self.anim_trigger: bool = False

    def update(self) -> None:
        super().update()
        self.check_anim_time()
        self.animate(self.images)

    def animate(self, images) -> None:
        if self.anim_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_anim_time(self) -> None:
        self.anim_trigger = False
        t_now = pg.time.get_ticks()
        if t_now - self.anim_time_prev > self.animation_time:
            self.anim_time_prev = t_now
            self.anim_trigger = True

    def get_images(self, path: str) -> deque:
        images = deque()

        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + "/" + file_name).convert_alpha()
                images.append(img)

        return images
