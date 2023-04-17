import math

from renderer.sprite_object import AnimatedSpriteObject


class Enemy:
    def __init__(self, game,
                 walk_forward_path: str, walk_left_path: str, walk_right_path: str, shoot_path: str, death_path: str,
                 animation_time: float, position: tuple[float, float], scale: float, shift: float,
                 damage: int, hit_chance: float, move_speed: float) -> None:
        self.game = game
        self.position: tuple[float, float] = position
        self.scale: float = scale
        self.shift: float = shift
        self.animation_time: float = animation_time
        self.damage: int = damage
        self.hit_chance: float = hit_chance
        self.move_speed: float = move_speed

        self.walk_forward_anim: AnimatedSpriteObject = self.make_animation(walk_forward_path)
        self.walk_left_anim: AnimatedSpriteObject = self.make_animation(walk_left_path)
        self.walk_right_anim: AnimatedSpriteObject = self.make_animation(walk_right_path)
        self.shoot_anim: AnimatedSpriteObject = self.make_animation(shoot_path)
        self.death_anim: AnimatedSpriteObject = self.make_animation(death_path)

        self.active_anim: AnimatedSpriteObject = self.walk_right_anim
    
    def make_animation(self, path: str) -> AnimatedSpriteObject:
        return AnimatedSpriteObject(self.game, path, self.animation_time, self.position, self.scale, self.shift)

    def movement(self) -> None:
        pass

    def move_towards(self, position: tuple[float, float]) -> None:
        px, py = position
        ox, oy = self.position
        dir = px - ox, py - oy
        mag = math.sqrt(dir[0] ** 2 + dir[1] ** 2)
        unit_dir = dir[0] / mag, dir[1] / mag
        new_pos = ox + unit_dir[0]  #####

    def update(self) -> None:
        self.active_anim.x, self.active_anim.y = self.position
        self.active_anim.update()
