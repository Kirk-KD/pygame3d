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
    def __init__(self, game, attack_distance: float, speed: float, health: int, damage: int, accuracy: float, 
                 base_path: str, anim_time: float, position: tuple[float, float], scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, base_path + "/idle", anim_time, position, scale, shift)

        self.attack_distance: float = attack_distance
        self.speed: float = speed
        self.healh: int = health
        self.damage: int = damage
        self.accuracy: float = accuracy

        self.alive: bool = True
        self.pain: bool = False

        self.idle_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/idle")
        self.walk_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/walk")
        self.attack_anim: deque = self.get_images("DOOM/resources/textures/sprites/" + base_path + "/attack")
    
    def logics(self) -> None:
        if not self.alive:
            return
        self.check_hit()
        if self.pain:
            self.animate_pain()
        else:
            self.animate(self.idle_anim)
    
    def animate_pain(self) -> None:
        self.animate(self.attack_anim)  # TODO
        if self.anim_trigger:
            self.pain = False

    def update(self) -> None:
        self.check_anim_time()
        self.get_sprite()
        self.logics()
    
    def check_hit(self) -> bool:
        if self.game.player.weapon_shot:
            if WIN_HALF_WIDTH - self.sprite_half_width < self.screen_x < WIN_HALF_WIDTH + self.sprite_half_width:
                self.game.player.weapon_shot = False
                self.pain = True
