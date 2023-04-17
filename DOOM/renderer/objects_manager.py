from renderer.sprite_object import SpriteObject, AnimatedSpriteObject


class ObjectInfo:
    def __init__(self, path: str, scale: float, shift: float, is_animated: bool = False, animation_time: float = -1) -> None:
        self.path: str = path
        self.scale: float = scale
        self.shift: float = shift
        self.is_animated: bool = is_animated
        self.animation_time: float = animation_time
    
    def make_at_position(self, game, position: tuple[float, float]) -> SpriteObject:
        if self.is_animated:
            return AnimatedSpriteObject(game, self.path, self.animation_time, position, self.scale, self.shift)
        else:
            return SpriteObject(game, self.path, position, self.scale, self.shift)


OBJECTS = {
    "barrel": ObjectInfo("barrel", 0.5, 0.3),
    "candle": ObjectInfo("candle", 0.75, 0.25),
    "torch_big_blue": ObjectInfo("torch_big_blue", 0.75, 0.25, is_animated=True, animation_time=120),
    "hanging_corpse_1": ObjectInfo("hanging_corpse_1", 1, 0)
}


class ObjectsManager:
    def __init__(self, game, objects: list[SpriteObject] = []) -> None:
        self.game = game
        self.objects = objects

    def add_sprite(self, sprite: SpriteObject) -> None:
        self.objects.append(sprite)
    
    def update(self) -> None:
        for obj in self.objects:
            obj.update()
