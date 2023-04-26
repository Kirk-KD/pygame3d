"""The representation of the Game.

This file defines the main `Game` class, and should only be used for 
the `Game` object from within `main.py`.
"""

# import pygame
import pygame as pg

# import all the rendering classes
from renderer.hud_renderer import HUDRenderer
from renderer.raycasting import Raycasting
from renderer.object_renderer import ObjectRenderer
from renderer.objects_manager import ObjectsManager

# import configurations
from config import *

# all other objects
from player import Player
from level import Level
from audio import AudioManager
from weapon import *


class Game:
    """An object that handles the initializing and running of the main game loop.

    The `Game` object is responsible for initializing the pygame library by 
    calling `pg.init()`, and also initializing all the objects used by the game, 
    such as the player and the level. The only public method that should be called 
    from the outside is `run()`. The `run` method should be only called from 
    `main.py`.

    Attributes:
        `title`: The game window's title.
        `clock`: Pygame Clock that is responsible for FPS and deltatime calculation.
        `deltatime`: Keep units consistent under different FPS.
        `running`: A flag that indicates whether or not the game is running.
        `surface`: Main window to draw the game on.
        `audio_manager`: Controls the music and plays sound effects.
        `hud_renderer`: Renders the HUD (heads up display).
        `player`: Represents the player.
        `object_renderer`: Renders most things, including walls, sky, ground, and sprites.
        `objects_manager`: Stores information about all objects such as enemies and sprites.
        `level`: Loads the level from a text file and a png file.
        `raycast`: Cast 2D rays that can be interpreted to create the pseudo-2D style walls.
    """

    def __init__(self, title: str) -> None:
        self.title: str = title

        self.__pre_init()

    def __pre_init(self) -> None:
        pg.init()

        self.clock: pg.time.Clock = pg.time.Clock()
        self.deltatime: float = None
        self.running: bool = False

        self.surface: pg.Surface = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_caption(self.title)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

    def __init(self) -> None:
        self.audio_manager: AudioManager = AudioManager()
        self.audio_manager.load("E1M1.mp3")
        self.hud_renderer: HUDRenderer = HUDRenderer(self)
        self.player: Player = Player(self)
        self.player.set_weapon(self.player.inventory.weapons[0])
        self.object_renderer: ObjectRenderer = ObjectRenderer(self)
        self.objects_manager: ObjectsManager = ObjectsManager(self)
        self.level: Level = Level("DOOM/resources/map_data/e1m1", self)
        self.raycast: Raycasting = Raycasting(self)
        
    def __frame(self) -> None:
        self.__events()
        self.__tick_delta()

        self.__update()
        self.__draw()

        pg.display.flip()
    
    def __update(self) -> None:
        """All updates that do not involve drawing to the screen go here. Should be called before `self.__draw()`."""

        self.raycast.update()
        self.objects_manager.update()
        self.hud_renderer.update()
        self.player.update()
    
    def __draw(self) -> None:
        self.object_renderer.draw()
        self.player.weapon.draw()
        self.hud_renderer.draw()

    def __events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__quit()

            self.player.single_weapon_fire(event)

    def run(self) -> None:
        self.__init()

        self.running = True

        self.audio_manager.play_music()
        while self.running:
            self.__frame()

    def __tick_delta(self) -> None:
        self.deltatime = self.clock.tick(FPS) / 1000

    def __quit(self) -> None:
        self.running = False
