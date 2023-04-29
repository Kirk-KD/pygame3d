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
from pickup import ShotgunPickup, ShellsPickup


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

        # initialize when this object is initialized
        self.__pre_init()

    def __pre_init(self) -> None:
        """Operatations to perform immedietly when this object is instantiated.

        Initializes pygame and setup other objects necessary for the game. This private function 
        sets the running flag, the Clock object, and the main game window. Also locks and hides 
        the mouse.
        """

        # initialize the pygame library
        pg.init()

        # clock for controlling the FPS
        self.clock: pg.time.Clock = pg.time.Clock()
        # deltatime that can be used to have fixed values across different FPS.
        self.deltatime: float = None
        # flag indicating if the game is running
        self.running: bool = False

        # main window to draw everything on
        self.surface: pg.Surface = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # set window title
        pg.display.set_caption(self.title)

        # lock the mouse
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

    def __init(self) -> None:
        """Objects to be setup before the game starts running.

        This function loads the level, sets up the audio and objects managers, the raycast 
        engine, and the objects and HUD renderers. Also sets up the player and gives the player a 
        weapon (pistol).
        """

        # create the audio manager and load music
        self.audio_manager: AudioManager = AudioManager()
        self.audio_manager.load("E1M1.mp3")

        # create the HUD renderer
        self.hud_renderer: HUDRenderer = HUDRenderer(self)

        # create the player
        self.player: Player = Player(self)
        self.player.set_weapon(self.player.inventory.weapons[0])

        # create the object renderer
        self.object_renderer: ObjectRenderer = ObjectRenderer(self)

        # create the objects manager
        self.objects_manager: ObjectsManager = ObjectsManager(self, pickups=[ShotgunPickup(self, (1.5, 15.5)), ShellsPickup(self, (2.5, 15.5))])

        # load level
        self.level: Level = Level("DOOM/resources/map_data/e1m1", self)

        # create the raycast engine
        self.raycast: Raycasting = Raycasting(self)
        
    def __frame(self) -> None:
        """Operations that should be ran in one frame in the main game loop.

        This method should be called in the main loop. It handles events, ticks 
        the FPS clock, update and draw objects and HUD graphics, and lastly updates 
        the display.
        """

        # poll events
        self.__events()
        # tick FPS
        self.__tick_delta()

        # update everything
        self.__update()
        # draw everything
        self.__draw()

        # update the display
        pg.display.flip()
    
    def __update(self) -> None:
        """Calls the update function of all objects that should be updated each frame."""

        # call update on everything
        self.raycast.update()
        self.objects_manager.update()
        self.hud_renderer.update()
        self.player.update()
    
    def __draw(self) -> None:
        """Calls the draw function of everything that should be drawn."""

        self.object_renderer.draw()
        self.player.weapon.draw()
        self.hud_renderer.draw()

    def __events(self) -> None:
        """Poll and handle events."""

        # loop through all event in one frame
        for event in pg.event.get():
            # quit to quit
            if event.type == pg.QUIT:
                # quit
                self.__quit()

            # shoot
            self.player.single_weapon_fire(event)

    def run(self) -> None:
        """
        Starts the game loop.

        This method initializes the game, sets running to True, and starts the game loop.
        """

        self.__init()

        # Start running the game loop
        self.running = True

        # Start playing the background music
        self.audio_manager.play_music()

        # Run the game loop until the game is no longer running
        while self.running:
            self.__frame()

    def __tick_delta(self) -> None:
        """
        Calculates the time between frames.

        This method calculates the time between frames using the Pygame clock object and sets it to self.deltatime.
        """

        self.deltatime = self.clock.tick(FPS) / 1000

    def __quit(self) -> None:
        """
        Quits the game.

        This method sets running to False, which stops the game loop.
        """
        
        self.running = False
