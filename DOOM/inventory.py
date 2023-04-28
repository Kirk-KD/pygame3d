from weapon import *


class Inventory:
    def __init__(self, game) -> None:
        self.game = game
        
        self.weapons: list = [Pistol(self.game)]

        self.key_red: bool = False
        self.key_yellow: bool = False
        self.key_blue: bool = False
    
    def has_weapon_at(self, index: int):
        return index < len(self.weapons)
    
    def add_weapon(self, weapon: Weapon):
        self.weapons.append(weapon)
