from __future__ import annotations

import pygame as pg
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from game import Game

from renderer.hud_renderer import HUDText
from config import WIN_WIDTH, WIN_HEIGHT


def fit_window(surf: pg.Surface):
    return pg.transform.scale(surf, (WIN_WIDTH, WIN_HEIGHT))


# text renderer
hud_text = HUDText()

# resources
skull = pg.transform.scale_by(pg.image.load("./DOOM/resources/textures/menu/skull.png"), 3)


class Button:
    """Class representing a button."""

    def __init__(self, x: int, y: int, text: str):
        self.x = x
        self.y = y
        self.position = x, y
        self.text = text

        self.surface = hud_text.string_to_surface(self.text, "small", 7)  # render the text once for better performance
        self.width, self.height = self.surface.get_size()  # get the text size
    
    def draw(self, menu, is_selected = False):
        """Draw the button"""

        if self.x is None:  # x is None, center x
            x = menu.surface.get_width() // 2 - self.width // 2
        else:
            x = self.x - self.width // 2
        
        if self.y is None:  # y is None, center y
            y = menu.surface.get_height() // 2 - self.height // 2
        else:
            y = self.y - self.height // 2

        menu.surface.blit(self.surface, (x, y))

        if is_selected:
            skull_x = x - 80
            menu.surface.blit(skull, (skull_x, y))
    
    def on_click(self, menu):
        """Implemented by children classes. Called when the player presses enter or space."""

        raise NotImplementedError


class Text:
    """Represents a text on the menu."""

    def __init__(self, text: str, x: int, y: int, scale: int):
        self.text: str = text
        self.x: int = x
        self.y: int = y
        self.scale: int = scale  # text scale
        self.surface: pg.Surface = hud_text.string_to_surface(self.text, "small", self.scale)  # render the text
        self.width, self.height = self.surface.get_size()  # get the text size
    
    def draw(self, menu):
        """Draw the text."""

        if self.x is None:  # center x
            x = menu.surface.get_width() // 2 - self.width // 2
        else:
            x = self.x - self.width // 2
        
        if self.y is None:  # center y
            y = menu.surface.get_height() // 2 - self.height // 2
        else:
            y = self.y - self.height // 2

        menu.surface.blit(self.surface, (x, y))


class MenuPage:
    def __init__(self, buttons: List[Button], texts: List[Text]):
        self.buttons = buttons
        self.texts = texts


class Menu:
    """Parent class for the menu."""

    def __init__(self, game, background: pg.Surface, page: MenuPage) -> None:
        self.game: Game = game
        self.background: pg.Surface = background
        self.surface: pg.Surface = self.game.surface  # main surface
        self.page: MenuPage = page

        self.selected_btn_idx: int = 0  # index of selected button
        self.selected_button: Button = self.page.buttons[0] if len(self.page.buttons) else None  # the selected button

    def events(self) -> bool:
        """Poll events, returns whether or not the game should quit."""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True

            if event.type == pg.KEYDOWN:  # key press
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:  # click a button
                    self.game.audio_manager.play(self.game.audio_manager.pistol)
                    self.selected_button.on_click(self)
                elif event.key == pg.K_UP:  # loop selections
                    self.next_button(-1)
                elif event.key == pg.K_DOWN:  # loop selections
                    self.next_button(1)
        
        return False

    def next_button(self, dir: int) -> None:
        if len(self.page.buttons):
            self.game.audio_manager.play(self.game.audio_manager.pistol)

            self.selected_btn_idx += dir
            self.selected_btn_idx %= len(self.page.buttons)
            self.selected_button = self.page.buttons[self.selected_btn_idx]
    
    def draw(self) -> None:
        self.surface.blit(self.background, (0, 0))

        for button in self.page.buttons:
            button.draw(self, button == self.selected_button)
        
        for text in self.page.texts:
            text.draw(self)
    
    def switch_page(self, new_page: MenuPage):
        self.page = new_page
        self.selected_btn_idx = 0
        self.selected_button = self.page.buttons[0] if len(self.page.buttons) else None
