from typing import List
import pygame as pg
from menu.menu import Menu, Button, Text, fit_window, MenuPage

background = fit_window(pg.image.load("./DOOM/resources/textures/menu/title_screen.png"))


class NewGame(Button):
    def __init__(self):
        super().__init__(None, 300, "new game")
    
    def on_click(self, menu):
        menu.game.new_game()


class Options(Button):
    def __init__(self):
        super().__init__(None, 380, "options")
    
    def on_click(self, menu):
        menu.switch_page(menu.options_page)


class ClassicControl(Button):
    def __init__(self):
        super().__init__(None, 460, "classic")
    
    def on_click(self, menu):
        menu.game.classic_control = True
        menu.switch_page(menu.main_page)


class ModernControl(Button):
    def __init__(self):
        super().__init__(None, 540, "modern")
    
    def on_click(self, menu):
        menu.game.classic_control = False
        menu.switch_page(menu.main_page)


class MainMenu(Menu):
    def __init__(self, game) -> None:
        self.main_page = MenuPage([
            NewGame(),
            Options()
        ], [])
        self.options_page = MenuPage([
            ClassicControl(),
            ModernControl()
        ], [
            Text("choose your control", None, 300, 7),
            Text("default is modern.", None, 360, 4)
        ])
        super().__init__(game, background, self.main_page, game.audio_manager.title_music_path)
