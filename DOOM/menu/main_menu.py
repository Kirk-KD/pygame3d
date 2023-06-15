from typing import List
import pygame as pg
from menu.menu import Menu, Button, Text


class StartButton(Button):
    def __init__(self):
        super().__init__(None, 300, "new game")
    
    def on_click(self, game):
        game.in_menu = False


class MainMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game, [
            StartButton()
        ], [])
