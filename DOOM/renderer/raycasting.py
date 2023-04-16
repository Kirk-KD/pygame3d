import pygame as pg
import math

from config import *
from player import Player
from map import Map
from renderer.texture import TextureData


class Raycasting:
    def __init__(self, game) -> None:
        self.game = game
        self.player: Player = self.game.player
        self.map: Map = self.game.map
        self.surf = self.game.surface

        self.textures: dict[int, TextureData] = self.game.object_renderer.wall_textures

        self.raycast_result: list[tuple] = []
        self.objs_to_render: list[tuple[float, pg.Surface, int]] = []
    
    def get_objects_to_render(self):
        self.objs_to_render = []
        for ray, values in enumerate(self.raycast_result):
            depth, proj_h, tex, offset = values

            if proj_h < WIN_HEIGHT:
                wall_col = self.textures[tex].texture.subsurface(offset * (TEX_SIZE - SCALE), 0, SCALE, TEX_SIZE)
                wall_col = pg.transform.scale(wall_col, (SCALE, proj_h))
                wall_pos = ray * SCALE, WIN_HALF_HEIGHT - proj_h // 2
            else:
                tex_h = TEX_SIZE * WIN_HEIGHT / proj_h
                wall_col = self.textures[tex].texture.subsurface(offset * (TEX_SIZE - SCALE), HALF_TEX_SIZE - tex_h // 2,
                                                                 SCALE, tex_h)
                wall_col = pg.transform.scale(wall_col, (SCALE, WIN_HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objs_to_render.append((depth, wall_col, wall_pos))

    def raycast(self):
        self.raycast_result = []

        ox, oy = self.player.position
        x_grid, y_grid = self.player.grid_position

        tex_vert, tex_hor = 1, 1

        ray_angle = self.player.angle - HALF_FOV + 0.0001
        for ray in range(RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_hor, dy = (y_grid + 1, 1) if sin_a > 0 else (y_grid - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if not self.map.unoccupied(*tile_hor):
                    tex_hor = self.map.map[tile_hor[1]][tile_hor[0]]
                    break

                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            x_vert, dx = (x_grid + 1, 1) if cos_a > 0 else (x_grid - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if not self.map.unoccupied(*tile_vert):
                    tex_vert = self.map.map[tile_vert[1]][tile_vert[0]]
                    break

                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, tex_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, tex_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.player.angle - ray_angle)

            proj_height = SCREEN_DISTANCE / (depth + 0.0001)

            self.raycast_result.append((depth, proj_height, texture, offset))

            # color = [255 / (1 + depth ** 7 * 0.00002)] * 3
            # pg.draw.rect(self.surf, color, (ray * SCALE, WIN_HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            ray_angle += DELTA_ANGLE
    
    def update(self) -> None:
        self.raycast()
        self.get_objects_to_render()
