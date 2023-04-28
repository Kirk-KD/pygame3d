from weapon import *


class Inventory:
    def __init__(self, game) -> None:
        self.game = game
        
        self.weapons: list = [Pistol(self.game)]

        self.key_red: bool = False
        self.key_yellow: bool = False
        self.key_blue: bool = False

    def get_by_type(self, weapon_type) -> Weapon:
        for weapon in self.weapons:
            if type(weapon) is weapon_type:
                return weapon
    
    def has_weapon_at(self, index: int) -> bool:
        return index < len(self.weapons)
    
    def add_weapon(self, weapon: Weapon) -> None:
        self.weapons.append(weapon)
