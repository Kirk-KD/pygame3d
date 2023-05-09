from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, List
if TYPE_CHECKING:
    from game import Game

import math
import random

from renderer.sprite_object import SpriteObject
from weapon import Pistol, Shotgun
from config import FPS, PICKUP_DISTANCE
from object_registry import ObjectRegistry

PICKUPS = ObjectRegistry()


class Pickup(SpriteObject):
    """An item pickup on the ground.
    
    This object inherits a `SpriteObject` for its 3D billboard style rendering.

    Attributes:
        (See inherited attributes in `SpriteObject`)
        `item_name` (`str`): The display name of this Pickup, display in the game HUD.
    """

    def __init__(self, game: Game, item_name: str, image_path: str | List[str], position: Tuple[float, float], scale: float = 1, shift: float = 0) -> None:
        super().__init__(game, image_path if type(image_path) is str else random.choice(image_path), position, scale, shift)

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


@PICKUPS.register
class ShotgunPickup(Pickup):
    NAME = "shotgun"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="the Shotgun", image_path="pickup/shotgun", position=position, scale=0.16, shift=3)
    
    def pick_up(self) -> bool:
        self.game.player.give_weapon(Shotgun(self.game))
        return True


@PICKUPS.register
class ClipPickup(Pickup):
    NAME = "clip"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="a Clip", image_path="pickup/clip", position=position, scale=0.14, shift=3.3)
    
    def pick_up(self) -> bool:
        pistol = self.game.player.inventory.get_by_type(Pistol)
        if not pistol.ammo_full():
            pistol.add_ammo(15)
            return True
        return False


@PICKUPS.register
class ShellsPickup(Pickup):
    NAME = "shells"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="4 Shotgun Shells", image_path="pickup/shells", position=position, scale=0.14, shift=3.3)
    
    def pick_up(self) -> bool:
        shotgun = self.game.player.inventory.get_by_type(Shotgun)
        if shotgun and not shotgun.ammo_full():
            shotgun.add_ammo(4)
            return True
        return False


@PICKUPS.register
class StimpackPickup(Pickup):
    NAME = "stimpack"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="a Stimpack", image_path=["pickup/stimpack_1", "pickup/stimpack_2", "pickup/stimpack_3"], position=position, scale=0.18, shift=2.6)
    
    def pick_up(self) -> bool:
        if self.game.player.health >= self.game.player.health_cap:
            return False
        
        self.game.player.heal(10)
        return True


@PICKUPS.register
class MedikitPickup(Pickup):
    NAME = "medikit"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="a Medikit", image_path=["pickup/medikit_1", "pickup/medikit_2", "pickup/medikit_3"], position=position, scale=0.2, shift=2.1)
    
    def pick_up(self) -> bool:
        if self.game.player.health >= self.game.player.health_cap:
            return False
        
        self.game.player.heal(25)
        return True


@PICKUPS.register
class GreenArmorPickup(Pickup):
    NAME = "armor_green"

    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="the Armor", image_path="pickup/armor_green", position=position, scale=0.3, shift=1.2)
    
    def pick_up(self) -> bool:
        if self.game.player.armor >= 100:
            return False
        
        self.game.player.set_armor(100)
        self.game.player.set_damage_reduction(0.3333)

        return True


@PICKUPS.register
class BlueArmorPickup(Pickup):
    NAME = "armor_blue"
    
    def __init__(self, game: Game, position: Tuple[float, float]) -> None:
        super().__init__(game, item_name="the Megaarmor", image_path="pickup/armor_blue", position=position, scale=0.3, shift=1.2)
    
    def pick_up(self) -> bool:
        if self.game.player.armor >= 200:
            return False
        
        self.game.player.set_armor(200)
        self.game.player.set_damage_reduction(0.5)

        return True
