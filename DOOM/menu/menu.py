import pygame as pg
from typing import List

from renderer.hud_renderer import HUDText


# text renderer
hud_text = HUDText()


class Button:
    """Class representing a button."""

    def __init__(self, x: int, y: int, text: str):
        self.x = x
        self.y = y
        self.position = x, y
        self.text = text

        self.surface = hud_text.string_to_surface(self.text, "small", 5)  # render the text once for better performance
        self.width, self.height = self.surface.get_size()  # get the text size
    
    def draw(self, menu):
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
    
    def on_click(self, game):
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


class Menu:
    """Parent class for the menu."""

    def __init__(self, game, buttons: List[Button], texts: List[Text]) -> None:
        self.game = game
        self.surface: pg.Surface = self.game.surface  # main surface
        self.buttons: List[Button] = buttons
        self.texts: List[Text] = texts

        self.selected_btn_idx: int = 0  # index of selected button
        self.selected_button: Button = self.buttons[0] if len(self.buttons) else None  # the selected button

    def events(self) -> bool:
        """Poll events, returns whether or not the game should quit."""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True

            if event.type == pg.KEYDOWN:  # key press
                if event.key == pg.K_KP_ENTER or event.key == pg.K_SPACE:  # click a button
                    self.selected_button.on_click(self.game)
                elif event.key == pg.K_UP:  # loop selections
                    if len(self.buttons):
                        self.selected_btn_idx -= 1
                        self.selected_btn_idx %= len(self.buttons)
                elif event.key == pg.K_DOWN:  # loop selections
                    if len(self.buttons):
                        self.selected_btn_idx += 1
                        self.selected_btn_idx %= len(self.buttons)
        
        return False
    
    def draw(self) -> None:
        for button in self.buttons:
            button.draw(self)
        
        for text in self.texts:
            text.draw(self)
