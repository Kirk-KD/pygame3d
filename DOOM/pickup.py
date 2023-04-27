import math

from renderer.sprite_object import SpriteObject
from weapon import Shotgun
from config import PICKUP_DISTANCE


class Pickup(SpriteObject):
    """An item pickup on the ground.
    
    This object inherits a `SpriteObject` for its 3D billboard style rendering.

    Attributes:
        (See inherited attributes in `SpriteObject`)
        `item_name` (`str`): The display name of this Pickup, display in the game HUD.
    """

    def __init__(self, game, item_name: str, image_path: str, position: tuple[float, float], scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, image_path, position, scale, shift)

        self.item_name: str = item_name
        self.pick_up_message: str = f"You picked up a {self.item_name}."

        self.deleted: bool = False
    
    def update(self) -> None:
        super().update()
        self.check_pick_up()
    
    def pick_up(self) -> None:
        raise NotImplementedError()

    def check_pick_up(self) -> None:
        if self.deleted:
            raise RuntimeWarning("Code should not reach here.")
        
        if math.hypot(self.game.player.x - self.x, self.game.player.y - self.y) <= PICKUP_DISTANCE:
            self.pick_up()
            self.deleted = True


class ShotgunPickup(Pickup):
    def __init__(self, game, position: tuple[float, float]) -> None:
        super().__init__(game, item_name="Shotgun", image_path="pickup/shotgun", position=position, scale=0.16, shift=3)
    
    def pick_up(self) -> None:
        self.game.player.give_weapon(Shotgun(self.game))
        print(self.pick_up_message)
