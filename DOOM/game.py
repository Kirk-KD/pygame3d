import pygame as pg

from config import *
from renderer.raycasting import Raycasting
from player import Player
from map import Map
from renderer.object_renderer import ObjectRenderer
from renderer.sprite_object import SpriteObject, AnimatedSpriteObject
from objects_manager import ObjectsManager


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
        self.map: Map = Map("DOOM/resources/map_data/map.txt")
        self.object_renderer = ObjectRenderer(self)
        self.raycast: Raycasting = Raycasting(self)
        self.object_manager: ObjectsManager = ObjectsManager(self, [
            SpriteObject(self, "candle", (2.5, 2.5), 0.75, 0.25),
            AnimatedSpriteObject(self, "torch_big_blue", 120, (5.5, 2.5), 0.75, 0.25)
        ])
        
    def __frame(self) -> None:
        self.__events()
        self.__tick_delta()

        self.__update()
        self.__draw()

        pg.display.flip()
    
    def __update(self) -> None:
        """All updates that do not involve drawing to the screen go here. Should be called before `self.__draw()`."""

        self.player.update()
        self.raycast.update()
        self.object_manager.update()
    
    def __draw(self) -> None:
        self.object_renderer.draw()

    def __events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__quit()

    def run(self) -> None:
        self.__init()

        self.running = True
        while self.running:
            self.__frame()

    def __tick_delta(self) -> None:
        self.deltatime = self.clock.tick(FPS) / 1000

    def __quit(self) -> None:
        self.running = False
