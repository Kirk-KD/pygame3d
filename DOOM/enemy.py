from collections import deque
import math

from config import *
from renderer.sprite_object import AnimatedSpriteObject


# class Enemy:
#     def __init__(self, game,
#                  walk_forward_path: str, walk_left_path: str, walk_right_path: str, shoot_path: str, death_path: str,
#                  animation_time: float, position: tuple[float, float], scale: float, shift: float,
#                  damage: int, hit_chance: float, move_speed: float, stop_distance: float, detection_distance: float) -> None:
#         self.game = game
#         self.position: tuple[float, float] = position
#         self.scale: float = scale
#         self.shift: float = shift
#         self.animation_time: float = animation_time
#         self.damage: int = damage
#         self.hit_chance: float = hit_chance
#         self.move_speed: float = move_speed

#         self.stop_distance: float = stop_distance
#         self.detection_distance: float = detection_distance

#         self.walk_forward_anim: AnimatedSpriteObject = self.make_animation(walk_forward_path)
#         self.walk_left_anim: AnimatedSpriteObject = self.make_animation(walk_left_path)
#         self.walk_right_anim: AnimatedSpriteObject = self.make_animation(walk_right_path)
#         self.shoot_anim: AnimatedSpriteObject = self.make_animation(shoot_path)
#         self.death_anim: AnimatedSpriteObject = self.make_animation(death_path)

#         self.active_anim: AnimatedSpriteObject = self.walk_right_anim

#         self.target_position: tuple[float, float] = None
    
#     def make_animation(self, path: str) -> AnimatedSpriteObject:
#         return AnimatedSpriteObject(self.game, path, self.animation_time, self.position, self.scale, self.shift)

#     def player_in_detection_distance(self) -> bool:
#         return math.hypot(self.game.player.x - self.position[0], self.game.player.y - self.position[1]) <= self.detection_distance

#     def movement(self) -> None:
#         if self.player_in_detection_distance():
#             # self.active_anim = self.walk_forward_anim
#             self.target_position = self.game.player.position
#             in_range = self.move_towards_target()
#             if in_range:
#                 self.active_anim = self.shoot_anim
#                 # TODO shoot
#             else:
#                 self.active_anim = self.walk_forward_anim

#     def move_towards_target(self, override_stop_dist: float = None) -> bool:
#         if not self.target_position:
#             return False
        
#         px, py = self.target_position
#         ox, oy = self.position

#         dx = px - ox
#         dy = py - oy
#         distance = math.sqrt(dx**2 + dy**2)

#         if distance < (self.stop_distance if override_stop_dist is None else override_stop_dist):
#             return True

#         speed_vector = (dx / distance * self.move_speed, dy / distance * self.move_speed)

#         self.position = ox + speed_vector[0], oy + speed_vector[1]
#         return False

#     def update(self) -> None:
#         self.active_anim.x, self.active_anim.y = self.position

#         self.movement()

#         self.active_anim.update()



class Enemy(AnimatedSpriteObject):
    def __init__(self, game, detection_distance: float, attack_distance: float, speed: float, health: int, damage: int, accuracy: float,  
                 base_path: str, anim_time: float, position: tuple[float, float], scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, base_path + "/idle", anim_time, position, scale, shift)

        self.detection_distance: float = detection_distance
        self.attack_distance: float = attack_distance
        self.speed: float = speed
        self.healh: int = health
        self.damage: int = damage
        self.accuracy: float = accuracy

        self.alive: bool = True

        self.pain: bool = False
        self.attack: bool = False

        self.player_in_range: bool = False
        self.can_see_player: bool = False

        self.idle_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/idle")
        self.walk_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/walk")
        self.attack_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/attack")
        self.pain_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/pain")
        self.death_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/death")

        self.frame_counter: int = 0
    
    def logics(self) -> None:
        if not self.alive:
            self.animate_death()
            return
        
        self.can_see_player = self.raycast_to_player()

        self.check_hit()
        self.check_death()
        self.check_attack()

        if self.pain:
            self.animate_pain()
        elif self.attack:
            self.animate_attack()
        else:
            self.animate(self.idle_anim)
    
    def animate_pain(self) -> None:
        self.animate(self.pain_anim)
        if self.anim_trigger:
            self.pain = False
    
    def animate_attack(self) -> None:
        self.animate(self.attack_anim)
        if self.anim_trigger:
            self.attack = False
    
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

                self.healh -= self.game.player.weapon.damage
    
    def check_death(self) -> None:
        if self.healh <= 0:
            self.alive = False
            self.death = True
    
    def check_attack(self) -> None:
        if math.hypot(self.game.player.x - self.x, self.game.player.y - self.y) < self.attack_distance and self.can_see_player and not self.pain:
            self.attack = True
    
    def raycast_to_player(self) -> bool:
        if self.grid_position == self.game.player.grid_position:
            return True  # no walls in a grid
        
        wall_d_vert, wall_d_hor = 0, 0
        player_d_vert, player_d_hor = 0, 0

        ox, oy = self.player.position
        x_grid, y_grid = self.player.grid_position

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

    @property
    def grid_position(self) -> tuple[int, int]:
        return int(self.x), int(self.y)
