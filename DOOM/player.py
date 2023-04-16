import math
import pygame as pg

from config import *


class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.angle: float = 0
        self.x, self.y = 1.5, 1.5
        self.diag_move_corr = 1 / math.sqrt(2)
        self.mouse_rel: float = 0
    
    def movement(self) -> None:
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_MOVE_SPEED * self.game.deltatime
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.deltatime
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.deltatime
        self.angle %= math.tau

    def check_collision(self, dx: float, dy: float) -> None:
        scale = PLAYER_SIZE_SCALE / self.game.deltatime
        if self.game.map.unoccupied(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.game.map.unoccupied(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self) -> None:
        self.mouse_rel = pg.mouse.get_rel()[0]
        self.mouse_rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.mouse_rel))
        self.angle += self.mouse_rel * MOUSE_SPEED
    
    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y
    
    @property
    def grid_position(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def update(self) -> None:
        self.movement()
        self.mouse_control()
