from weapon import *


class Inventory:
    def __init__(self, game) -> None:
        self.game = game
        
        self.weapons: list = [Pistol(self.game)]

        self.key_red: bool = False
        self.key_yellow: bool = False
        self.key_blue: bool = False
