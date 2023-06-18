"""The representation of the Game.

This file defines the main `Game` class, and should only be used for 
the `Game` object from within `main.py`.
"""

# import pygame
import pygame as pg

import datetime

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
from menu.menu import Menu
from menu.main_menu import MainMenu


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

        # game didn't start yet, in menu
        self.in_menu: bool = False

        # game options
        self.classic_control: bool = False
        self.difficulty: int = 2

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

        # flag for ctrl key
        self.ctrl: bool = False

        # level timer
        self.start_time: datetime.datetime = None
        self.finish_time: datetime.datetime = None
        self.seconds: float = None

    def __init(self) -> None:
        """Objects to be setup before the game starts running.

        This function loads the level, sets up the audio and objects managers, the raycast 
        engine, and the objects and HUD renderers. Also sets up the player and gives the player a 
        weapon (pistol).
        """

        # create the audio manager and load music
        self.audio_manager: AudioManager = AudioManager()

        # load the menu
        self.open_menu(MainMenu(self))

    def play(self, died: bool = False) -> None:
        # create the HUD renderer
        self.hud_renderer: HUDRenderer = HUDRenderer(self)

        # create the player
        self.player: Player = Player(self)
        self.player.set_weapon(self.player.inventory.weapons[0])

        # create the object renderer
        self.object_renderer: ObjectRenderer = ObjectRenderer(self)

        # create the objects manager
        self.objects_manager: ObjectsManager = ObjectsManager(self)

        # load level
        self.level: Level = Level("DOOM/resources/map_data/e1m1", self)

        # create the raycast engine
        self.raycast: Raycasting = Raycasting(self)

        # counters
        if not died:
            self.deaths: int = 0
        self.kills: int = 0
        self.shots_fired: int = 0
        self.shots_hit: int = 0

        # start timer
        self.start_timer()

    def __frame(self) -> None:
        """Operations that should be ran in one frame in the main game loop.

        This method should be called in the main loop. It handles events, ticks 
        the FPS clock, update and draw objects and HUD graphics, and lastly updates 
        the display.
        """

        if self.in_menu:
            self.running = (not self.menu.events()) and self.running
            if self.running:
                self.menu.draw()
        else:
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

        if self.player.is_dead:
            s = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
            s.set_alpha(128)
            s.fill((255, 0, 0))
            self.surface.blit(s, (0, 0))

            text = self.hud_renderer.hud_text.string_to_surface("you died", "small", 9)
            text_x = WIN_HALF_WIDTH - text.get_width() // 2
            text_y = WIN_HALF_HEIGHT - text.get_height()
            self.surface.blit(text, (text_x, text_y))

            text2 = self.hud_renderer.hud_text.string_to_surface("press enter or space to restart", "small", 3)
            text2_x = WIN_HALF_WIDTH - text2.get_width() // 2
            text2_y = WIN_HALF_HEIGHT + text2.get_height()
            self.surface.blit(text2, (text2_x, text2_y))

    def __events(self) -> None:
        """Poll and handle events."""

        # loop through all event in one frame
        for event in pg.event.get():
            # quit to quit
            if event.type == pg.QUIT:
                # quit
                self.quit()
            
            # key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                    self.ctrl = True
                
                if self.player.is_dead:
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.play(died=True)
                elif event.key == pg.K_SPACE:
                    self.player.use_lever()
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                    self.ctrl = False

            # shoot
            self.player.single_weapon_fire(event)
        
        if self.ctrl:
            self.player.shoot()

    def run(self) -> None:
        """
        Starts the game loop.

        This method initializes the game, sets running to True, and starts the game loop.
        """

        self.__init()

        # Start running the game loop
        self.running = True

        # Start playing the background music
        self.audio_manager.play_music(self.audio_manager.title_music_path)

        # Run the game loop until the game is no longer running
        while self.running:
            self.__frame()
    
    def new_game(self) -> None:
        self.in_menu = False
        self.audio_manager.play_music(self.audio_manager.music_path)

        self.play()

    def __tick_delta(self) -> None:
        """
        Calculates the time between frames.

        This method calculates the time between frames using the Pygame clock object and sets it to self.deltatime.
        """

        self.deltatime = self.clock.tick(FPS) / 1000

    def quit(self) -> None:
        """
        Quits the game.

        This method sets running to False, which stops the game loop.
        """
        
        self.running = False

    def open_menu(self, menu: Menu) -> None:
        self.in_menu = True
        self.menu = menu
        self.audio_manager.play_music(menu.music_path)

    def start_timer(self) -> None:
        self.start_time = datetime.datetime.now()
        self.finish_time = None
        self.seconds = None

    def stop_timer(self) -> None:
        self.finish_time = datetime.datetime.now()
        self.seconds = (self.finish_time - self.start_time).total_seconds()

    @property
    def kills_percentage(self) -> float:
        return self.kills / self.level.total_enemies * 100
