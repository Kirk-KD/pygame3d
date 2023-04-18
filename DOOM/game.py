import pygame as pg

from config import *
from renderer.raycasting import Raycasting
from player import Player
from level import Level
from renderer.object_renderer import ObjectRenderer
from renderer.objects_manager import ObjectsManager
from weapon import *
from enemy import Enemy


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
        self.player: Player = Player(self)
        self.player.set_weapon(Pistol(self))
        self.object_renderer = ObjectRenderer(self)
        self.objects_manager: ObjectsManager = ObjectsManager(self, enemies=[Enemy(self, 5, 3, 100, 10, 0.3, "enemies/zombieman", 200, (1.5, 1.5), 0.75, 0.35)])
        self.level: Level = Level("DOOM/resources/map_data/map2.txt", self)
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
        self.player.update()
    
    def __draw(self) -> None:
        self.object_renderer.draw()
        self.player.weapon.draw()

    def __events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__quit()

            self.player.single_weapon_fire(event)

    def run(self) -> None:
        self.__init()

        self.running = True
        while self.running:
            self.__frame()

    def __tick_delta(self) -> None:
        self.deltatime = self.clock.tick(FPS) / 1000

    def __quit(self) -> None:
        self.running = False
