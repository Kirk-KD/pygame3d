from typing import List
import pygame as pg
from menu.menu import Menu, Button, Text, fit_window, MenuPage

background = fit_window(pg.image.load("./DOOM/resources/textures/menu/title_screen.png"))


class NewGame(Button):
    def __init__(self):
        super().__init__(None, 300, "new game")
    
    def on_click(self, menu):
        menu.switch_page(menu.difficulty_page)


class ImTooYoungToDie(Button):
    def __init__(self):
        super().__init__(None, 320, "i'm too young to die!", 5)
    
    def on_click(self, menu):
        menu.game.difficulty = 0
        menu.game.new_game()


class HeyNotTooRough(Button):
    def __init__(self):
        super().__init__(None, 380, "hey, not too rough.", 5)
    
    def on_click(self, menu):
        menu.game.difficulty = 1
        menu.game.new_game()


class HurtMePlenty(Button):
    def __init__(self):
        super().__init__(None, 440, "hurt me plenty.", 5)
    
    def on_click(self, menu):
        menu.game.difficulty = 2
        menu.game.new_game()


class UltraViolence(Button):
    def __init__(self):
        super().__init__(None, 500, "ultra-violence.", 5)
    
    def on_click(self, menu):
        menu.game.difficulty = 3
        menu.game.new_game()


class Nightmare(Button):
    def __init__(self):
        super().__init__(None, 580, "nightmare!", 10)
    
    def on_click(self, menu):
        menu.game.difficulty = 4
        menu.game.new_game()


class Options(Button):
    def __init__(self):
        super().__init__(None, 380, "options")
    
    def on_click(self, menu):
        menu.switch_page(menu.options_page)


class Quit(Button):
    def __init__(self):
        super().__init__(None, 460, "quit")
    
    def on_click(self, menu: Menu):
        menu.game.quit()


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
            Options(),
            Quit()
        ], [])
        self.options_page = MenuPage([
            ClassicControl(),
            ModernControl()
        ], [
            Text("choose your control:", None, 300, 7),
            Text("default is modern.", None, 360, 4)
        ])
        self.difficulty_page = MenuPage([
            ImTooYoungToDie(),
            HeyNotTooRough(),
            HurtMePlenty(),
            UltraViolence(),
            Nightmare()
        ], [
            Text("choose skill level:", None, 200, 5)
        ], default_button_idx=2)
        super().__init__(game, background, self.main_page, game.audio_manager.title_music_path)
