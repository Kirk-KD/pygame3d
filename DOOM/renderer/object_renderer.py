"""Defines the object that is responsible for rendering all objects.

The only thing that should be exported from the file is the `ObjectRenderer`,
which renders the ground, sky, walls, enemies, and decorations.
"""

# import pygame and os for iterating in a directory
import pygame as pg
import os

from config import *
from renderer.texture import TextureData


class ObjectRenderer:
    """Renders the ground, sky, walls, enemies, and decorations.

    This object first loads all the textures before the game starts. It also 
    draws most objects in the game. Objects are read from the `objs_to_render` 
    property from the raycast object.
    """

    WALL_TEXTURES_KEYS = []

    def __init__(self, game) -> None:
        """Initializes the object renderer."""

        # take in the game
        self.game = game
        # short name for quick access
        self.surface: pg.Surface = game.surface
        # load the wall textures
        self.wall_textures: dict[int, TextureData] = self.load_wall_textures()
        # get all the wall texture keys
        ObjectRenderer.WALL_TEXTURES_KEYS = list(self.wall_textures.keys())

        # let the sky texture be empty for now
        self.sky_texture: TextureData = None
        self.sky_offset: float = 0
    
    def draw(self) -> None:
        """Draw the sky, the ground, and lastly the objects."""

        # render sky
        self.render_sky()
        # render ground
        self.render_ground()
        # render objects
        self.render_objects()
    
    def render_objects(self) -> None:
        """Render objects."""

        # draw the objects from the farthest to the closest, so the nearer objects will cover the farther ones.
        objs = sorted(self.game.raycast.objs_to_render, reverse=True, key=lambda o: o[0])

        # loop through and unpack the objects into the depth (z), image, and on-screen position
        for depth, image, pos in objs:
            # calculate the darkness from the depth
            color = [min(255 / (1 + depth ** 5 * 0.00001), 230)] * 3
            # darken the image to be drawn
            image.fill(color, special_flags=pg.BLEND_RGB_MULT)
            # draw the image on the main window
            self.surface.blit(image, pos)

    def render_sky(self) -> None:
        """Draw the sky."""

        # calculate and update the sky x coordinate based on mouse movement
        self.sky_offset = (self.sky_offset + 1.5 * self.game.player.mouse_rel) % WIN_WIDTH
        # draw the two sky textures to create a seemless skybox.
        self.surface.blit(self.sky_texture.texture, (-self.sky_offset, 0))
        self.surface.blit(self.sky_texture.texture, (-self.sky_offset + WIN_WIDTH, 0))
    
    def render_ground(self) -> None:
        """Render the ground."""

        # draw the ground (lower half of the screen)
        pg.draw.rect(self.surface, (30, 30, 30), (0, WIN_HALF_HEIGHT, WIN_WIDTH, WIN_HEIGHT))

    def load_wall_textures(self) -> dict[str, TextureData]:
        """Load all the wall textures."""

        # dictionary of the wall textures
        walls = {}
        # base directory of the wall textures
        base = "DOOM/resources/textures/walls/"
        # loop through all the wall texture files
        for path in os.listdir(base):
            # map the TextureData to the file name
            walls[path.split(".")[0]] = TextureData(base + path)
        # return the read wall textures
        return walls

    def load_sky_texture(self, file_name: str) -> None:
        """Load the sky texture"""

        # read and store the sky texture
        self.sky_texture = TextureData(f"DOOM/resources/textures/skies/{file_name}.png", (WIN_WIDTH, WIN_HALF_HEIGHT))
        # darken the sky a little
        self.sky_texture.texture.fill((210, 210, 210), special_flags=pg.BLEND_RGB_MULT)
