from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from game import Game

import random
import pygame as pg
from collections import deque
import math

from config import *
from renderer.sprite_object import AnimatedSpriteObject
from object_registry import ObjectRegistry
from pickup import PICKUPS

ENEMIES = ObjectRegistry()


class Enemy(AnimatedSpriteObject):
    def __init__(self, game: Game, detection_distance: float, attack_distance: float, speed: float, health: int, damage: int, accuracy: float,  
                 base_path: str, attack_frame_index: int, anim_time: float, position: Tuple[float, float],
                 attack_sound: pg.mixer.Sound, idle_sound: pg.mixer.Sound, death_sound: pg.mixer.Sound, hurt_sound: pg.mixer.Sound,
                 scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, base_path + "/idle", anim_time, position, scale, shift)

        self.detection_distance: float = detection_distance * DIFFICULTY_RANGE_SCALING[self.game.difficulty]
        self.attack_distance: float = attack_distance * DIFFICULTY_RANGE_SCALING[self.game.difficulty]
        self.speed: float = speed
        self.health: int = health
        self.damage: int = round(damage * DIFFICULTY_DAMAGE_SCALING[self.game.difficulty])
        self.accuracy: float = accuracy * DIFFICULTY_ACCURACY_SCALING[self.game.difficulty]

        self.alive: bool = True

        self.pain: bool = False
        self.attack: bool = False
        self.walk: bool = False

        self.player_in_range: bool = False
        self.can_see_player: bool = False

        self.idle_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/idle")
        self.walk_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/walk")
        self.attack_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/attack")
        self.pain_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/pain")
        self.death_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/death")

        self.attack_sound: pg.mixer.Sound = attack_sound
        self.idle_sound: pg.mixer.Sound = idle_sound
        self.death_sound: pg.mixer.Sound = death_sound
        self.hurt_sound: pg.mixer.Sound = hurt_sound

        self.attack_frame: pg.Surface = self.attack_anim[attack_frame_index]

        self.frame_counter: int = 0

        self.target_position: Tuple = None
    
    def logics(self) -> None:
        if not self.alive:
            self.animate_death()
            return
        
        if self.game.player.health <= 0:
            return

        self.can_see_player = self.raycast_to_player()

        in_detection = self.player_in_detection_distance()
        in_attack = self.player_in_attack_distance()

        if in_detection:
            if in_attack:
                if self.can_see_player:
                    pass
                else:
                    self.pathfind()
                    self.movement()
            else:
                if self.can_see_player:
                    self.target_position = self.game.player.position
                    self.movement()
                else:
                    self.pathfind()
                    self.movement()

        self.check_hit()
        self.check_death()
        self.check_attack()

        if self.pain:
            self.animate_pain()
        elif self.attack:
            self.animate_attack()
        elif self.walk:
            self.animate_walk()
        else:
            self.animate_idle()

    def check_collision(self, dx: float, dy: float) -> None:
        scale = ENEMY_SIZE_SCALE / self.game.deltatime
        if self.game.level.map.unoccupied(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.game.level.map.unoccupied(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def movement(self) -> None:
        if self.target_position is None:
            return
        
        if self.attack:
            return
        
        self.walk = True
        
        tx, ty = self.target_position
        angle = math.atan2(ty + 0.5 - self.y, tx + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_collision(dx, dy)
    
    def animate_idle(self) -> None:
        self.animate(self.idle_anim)
        if self.anim_trigger:
            if random.random() <= 0.2:
                self.play_sound(self.idle_sound)

    def animate_pain(self) -> None:
        self.animate(self.pain_anim)
        if self.anim_trigger:
            self.pain = False
    
    def animate_attack(self) -> None:
        self.animate(self.attack_anim)
        if self.anim_trigger:
            self.attack = False
            if self.image == self.attack_frame:
                self.play_sound(self.attack_sound)

                if random.random() <= self.accuracy:
                    self.game.player.take_damage(self.damage)
    
    def animate_walk(self) -> None:
        self.animate(self.walk_anim)
        if self.anim_trigger:
            self.walk = False
    
    def animate_death(self) -> None:
        if not self.alive:
            if self.anim_trigger and self.frame_counter < len(self.death_anim) - 1:
                self.death_anim.rotate(-1)
                self.image = self.death_anim[0]
                self.frame_counter += 1

    def update(self) -> None:
        self.check_anim_time()
        self.get_sprite()
        self.logics()
    
    def check_hit(self) -> None:
        if self.game.player.weapon_shot and self.can_see_player:
            if WIN_HALF_WIDTH - self.sprite_half_width < self.screen_x < WIN_HALF_WIDTH + self.sprite_half_width:
                self.game.player.weapon_shot = False
                self.pain = True

                self.health -= self.game.player.weapon.damage

                self.game.shots_hit += 1

                if self.health > 0:
                    self.play_sound(self.hurt_sound)
    
    def check_death(self) -> None:
        if self.health <= 0:
            self.alive = False
            self.death = True

            self.play_sound(self.death_sound)

            self.drop_loot()

            self.game.kills += 1
    
    def check_attack(self) -> None:
        if self.player_in_attack_distance() and self.can_see_player and not self.pain:
            self.attack = True
    
    def raycast_to_player(self) -> bool:
        if self.grid_position == self.game.player.grid_position:
            return True  # no walls in a grid
        
        wall_d_vert, wall_d_hor = 0, 0
        player_d_vert, player_d_hor = 0, 0

        ox, oy = self.game.player.position
        x_grid, y_grid = self.game.player.grid_position

        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        y_hor, dy = (y_grid + 1, 1) if sin_a > 0 else (y_grid - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.grid_position:
                player_d_hor = depth_hor
                break
            if not self.game.level.map.unoccupied(*tile_hor):
                wall_d_hor = depth_hor
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
            if tile_vert == self.grid_position:
                player_d_vert = depth_vert
                break
            if not self.game.level.map.unoccupied(*tile_vert):
                wall_d_vert = depth_vert
                break

            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_d_vert, player_d_hor)
        wall_dist = max(wall_d_vert, wall_d_hor)

        return 0 < player_dist < wall_dist or wall_dist == 0

    def player_in_detection_distance(self) -> bool:
        return math.hypot(self.game.player.x - self.x, self.game.player.y - self.y) < self.detection_distance

    def player_in_attack_distance(self) -> bool:
        return math.hypot(self.game.player.x - self.x, self.game.player.y - self.y) < self.attack_distance

    def pathfind(self) -> None:
        xy = self.game.level.map.astar_next(self.grid_position, self.game.player.grid_position)
        if not xy:
            return
        x, y = xy
        self.target_position = x + 0.5, y + 0.5

    @property
    def grid_position(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    def drop_loot(self) -> None:
        loots = ["clip", "shells", "stimpack", "medikit", "armor_green", "armor_blue", None]
        weights = [0.45, 0.35, 0.1, 0.05, 0.02, 0.01, 1]
        loot_name = random.choices(loots, weights, k=1)[0]

        if loot_name is not None:
            self.game.objects_manager.add_pickup(PICKUPS.get(loot_name)(self.game, self.position))

    def calculate_volume(self) -> float:
        distance = math.dist(self.game.player.position, self.position)
        if distance > SOUND_MAX_DISTANCE:
            return 0
        
        volume = 1 - distance / SOUND_MAX_DISTANCE

        px, py = self.game.player.position
        dx = self.x - px
        dy = self.y - py
        angle_player_to_enemy = math.atan2(dy, dx)
        angle_difference = abs((angle_player_to_enemy - self.game.player.angle + math.pi) % (2 * math.pi) - math.pi)

        volume *= (math.pi - angle_difference / 1.5) / math.pi
        return volume

    def play_sound(self, sound: pg.mixer.Sound) -> None:
        self.game.audio_manager.play(sound, self.calculate_volume())


@ENEMIES.register
class Zombieman(Enemy):
    NAME = "zombieman"

    def __init__(self, game: Game, position: Tuple[float, float]):
        super().__init__(game=game,
                         detection_distance=12,
                         attack_distance=7,
                         speed=0.03,
                         health=100,
                         damage=10,
                         accuracy=0.45,
                         base_path="enemies/zombieman",
                         attack_frame_index=1,
                         anim_time=200,
                         position=position,
                         scale=0.7,
                         shift=0.25,
                         attack_sound=game.audio_manager.enemy_attack,
                         idle_sound=game.audio_manager.enemy_idle,
                         death_sound=game.audio_manager.enemy_death,
                         hurt_sound=game.audio_manager.enemy_hurt)
