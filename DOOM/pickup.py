from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from game import Game

import math

from renderer.sprite_object import SpriteObject
from weapon import Pistol, Shotgun
from config import FPS, PICKUP_DISTANCE


class Pickup(SpriteObject):
    """An item pickup on the ground.
    
    This object inherits a `SpriteObject` for its 3D billboard style rendering.

    Attributes:
        (See inherited attributes in `SpriteObject`)
        `item_name` (`str`): The display name of this Pickup, display in the game HUD.
    """

    def __init__(self, game: Game, item_name: str, image_path: str, position: Tuple[float, float], scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, image_path, position, scale, shift)

        self.item_name: str = item_name
        self.pick_up_message: str = f"Picked up {self.item_name}."

        self.deleted: bool = False
    
    def update(self) -> None:
        super().update()
        self.check_pick_up()
    
    def pick_up(self) -> bool:
        """
        Function that should be implemented by children classes. Defines action when this is picked up.

        Returns:
            Whether or not the item was actually picked up.
        """
        raise NotImplementedError()

    def check_pick_up(self) -> None:
        """Check if this item can be picked up.

        If the item was picked up, set the `deleted` property to True.
        """
        if math.hypot(self.game.player.x - self.x, self.game.player.y - self.y) <= PICKUP_DISTANCE:
            if self.pick_up():
                self.game.hud_renderer.console(self.pick_up_message, FPS * 2.5)
                self.deleted = True


class ShotgunPickup(Pickup):
    def __init__(self, game: Game, position: tuple[float, float]) -> None:
        super().__init__(game, item_name="the Shotgun", image_path="pickup/shotgun", position=position, scale=0.16, shift=3)
    
    def pick_up(self) -> bool:
        self.game.player.give_weapon(Shotgun(self.game))
        return True


class ClipPickup(Pickup):
    def __init__(self, game: Game, position: tuple[float, float]) -> None:
        super().__init__(game, item_name="a Clip", image_path="pickup/clip", position=position, scale=0.14, shift=3.3)
    
    def pick_up(self) -> bool:
        pistol = self.game.player.inventory.get_by_type(Pistol)
        if not pistol.ammo_full():
            pistol.add_ammo(15)
            return True
        return False


class ShellsPickup(Pickup):
    def __init__(self, game: Game, position: tuple[float, float]) -> None:
        super().__init__(game, item_name="4 Shotgun Shells", image_path="pickup/shells", position=position, scale=0.14, shift=3.3)
    
    def pick_up(self) -> bool:
        shotgun = self.game.player.inventory.get_by_type(Shotgun)
        if shotgun and not shotgun.ammo_full():
            shotgun.add_ammo(4)
            return True
        return False
