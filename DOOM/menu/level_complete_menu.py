import pygame as pg

from menu.menu import MenuPage, Menu, Text, fit_window

background = fit_window(pg.image.load("./DOOM/resources/textures/menu/level_complete.png"))


class LevelCompleteMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game, background, MenuPage(
            [], [
                Text("level complete!", None, 100, 7),
                Text(f"{round(game.seconds, 2)} seconds", None, 250, 5),
                Text(f"kills: {game.kills} ({round(game.kills_percentage)}%)", None, 325, 5),
                Text(f"deaths: {game.deaths}", None, 400, 5),
                Text(f"shots: {game.shots_fired}", None, 475, 5),
                Text(f"hits: {game.shots_hit} ({round(game.shots_hit / game.shots_fired * 100)}%)", None, 550, 5)
            ]
        ), game.audio_manager.level_complete_music_path)
