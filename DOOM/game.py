import pygame as pg

from renderer.hud_renderer import HUDRenderer
from config import *
from renderer.raycasting import Raycasting
from player import Player
from level import Level
from renderer.object_renderer import ObjectRenderer
from renderer.objects_manager import ObjectsManager
from audio import AudioManager
from weapon import *


class Game:
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
        self.player.set_weapon(Pistol(self))
        self.object_renderer: ObjectRenderer = ObjectRenderer(self)
        # self.objects_manager: ObjectsManager = ObjectsManager(self, enemies=[Enemy(self, 15, 6, 1, 100, 10, 0.3, "enemies/zombieman", 200, (14.5, 13.5), 0.7, 0.25)])
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
