from renderer.sprite_object import SpriteObject, AnimatedSpriteObject


class ObjectsManager:
    def __init__(self, game, objects: list[SpriteObject] = []) -> None:
        self.game = game
        self.objects = objects

    def add_sprite(self, sprite: SpriteObject) -> None:
        self.objects.append(sprite)
    
    def update(self) -> None:
        for obj in self.objects:
            obj.update()
