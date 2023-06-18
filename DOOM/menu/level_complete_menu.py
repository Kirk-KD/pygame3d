import pygame as pg

from menu.menu import MenuPage, Menu, Button, Text, fit_window
from menu import main_menu

background = fit_window(pg.image.load("./DOOM/resources/textures/menu/level_complete.png"))


class Continue(Button):
    def __init__(self):
        super().__init__(None, 700, "continue")
    
    def on_click(self, menu: Menu):
        menu.switch_page(menu.options_page)


class NextLevel(Button):
    def __init__(self):
        super().__init__(None, 250, "next level")
    
    def on_click(self, menu: Menu):
        menu.game.new_game()


class RestartLevel(Button):
    def __init__(self):
        super().__init__(None, 350, "restart level")
    
    def on_click(self, menu: Menu):
        menu.game.new_game()


class MainMenu(Button):
    def __init__(self):
        super().__init__(None, 450, "main menu")
    
    def on_click(self, menu: Menu):
        menu.game.open_menu(main_menu.MainMenu(menu.game))


class Quit(Button):
    def __init__(self):
        super().__init__(None, 550, "quit")
    
    def on_click(self, menu: Menu):
        menu.game.quit()


class LevelCompleteMenu(Menu):
    def __init__(self, game) -> None:
        self.summary_page = MenuPage(
            [Continue()], [
                Text("level complete!", None, 100, 7),
                Text(f"{round(game.seconds, 2)} seconds", None, 250, 5),
                Text(f"kills: {game.kills} ({round(game.kills_percentage)}%)", None, 325, 5),
                Text(f"deaths: {game.deaths}", None, 400, 5),
                Text(f"shots: {game.shots_fired}", None, 475, 5),
                Text(f"hits: {game.shots_hit} ({round(game.shots_hit / game.shots_fired * 100)}%)", None, 550, 5)
            ]
        )
        self.options_page = MenuPage(
            [
                NextLevel(),
                RestartLevel(),
                MainMenu(),
                Quit()
            ], []
        )
        super().__init__(game, background, self.summary_page, game.audio_manager.level_complete_music_path)
