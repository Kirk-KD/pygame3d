"""
This module contains the implementation of the Level class, which represents a game level.

The Level class loads a map from a PNG image file and a set of game objects and enemies from a text file.
It also initializes the game player's position and rotation angle, as well as the sky texture used for rendering.

Usage:
    from level import Level
    level = Level("path/to/level", game)  # create a new Level instance (automatically loads the level from the path.)
"""

# import math
import math

# import other things
from map import Map
from png_map import PNGMap
from renderer.sprite_object import SpriteObject
from renderer.objects_manager import OBJECTS
from enemy import ENEMIES

# define keywords
OBJECT = "object "
OBJECT_END = "object end"
ENEMY = "enemy "
ENEMY_END = "enemy end"
SKY = "sky "
PLAYER = "player "


class Level:
    """
    A class representing a game level.

    Attributes:
        `path` (str): The path to the level file.
        `game` (Game): The game object.
        `objects_manager` (ObjectsManager): The game's objects manager.
        `png_map` (PNGMap): The PNG map object.
        `map` (Map): The map object.
        `sprite_objects` (list[SpriteObject]): The list of sprite objects.
    """

    def __init__(self, path: str, game) -> None:
        """
        Constructs a Level object.

        Args:
            path (str): The path to the level file.
            game (Game): The game object.
        """

        self.path: str = path
        self.game = game
        self.objects_manager = game.objects_manager

        self.png_map: PNGMap = PNGMap(self.path + ".png")
        self.map: Map = Map()
        self.sprite_objects: list[SpriteObject] = []

        self.load()
    
    def load(self) -> None:
        """
        Loads the level file.

        Raises:
            Exception: when the map file read is not in a correct format.
        """

        # read the level file
        with open(self.path + ".txt", "r") as f:
            lines = f.read().split("\n")

        object_name = None
        enemy_name = None
        sky_name = None
        player_pos = None

        # go through all lines of the file
        for lineno, line in enumerate(lines):
            print("Read:", line)

            # ignore empty or comment (#) lines
            if len(line) == 0 or line.startswith("#"):
                continue

            # if user is ending an object definition
            if line == OBJECT_END:
                if object_name is None:
                    raise Exception("No object definition to end!")

                object_name = None
                continue

            # user is starting an object definition
            if line.startswith(OBJECT):
                object_name = line[len(OBJECT):]
                if object_name not in OBJECTS:
                    raise Exception(f"No object named '{object_name}' found!")
                continue
                
            # object is setting player position and rotation
            if line.startswith(PLAYER):
                if player_pos is not None:
                    raise Exception("Cannot define player spawn pos twice!")
                p = line[len(PLAYER):].split()
                player_pos = float(p[0]), float(p[1])
                player_rot = math.radians(float(p[2]) + 85)
                continue

            # during an object definition
            if object_name:
                obj_x, obj_y = line.strip().split()
                obj_x, obj_y = float(obj_x), float(obj_y)
                self.objects_manager.add_sprite(OBJECTS[object_name].make_at_position(self.game, (float(obj_x), float(obj_y))))
                continue

            # ending an enemy definition
            if line == ENEMY_END:
                enemy_name = None
                continue

            # starting an enemy definition
            if line.startswith(ENEMY):
                if enemy_name is not None:
                    raise Exception(f"Didn't end enemy def!")

                enemy_name = line[len(ENEMY):]
                if enemy_name not in ENEMIES:
                    raise Exception(f"No enemy named '{enemy_name}'!")
                
                continue

            # setting sky texture
            if line.startswith(SKY):
                if sky_name is not None:
                    raise Exception(f"Already defined sky!")
                
                sky_name = line[len(SKY):]

            # during an enemy definition
            if enemy_name:
                enemy_x, enemy_y = line.strip().split()
                enemy_x, enemy_y = float(enemy_x), float(enemy_y)
                self.objects_manager.add_enemy(ENEMIES[enemy_name](self.game, (enemy_x, enemy_y)))
                continue
        
        self.map.load(self.png_map.to_map())
        if player_pos:
            self.game.player.x, self.game.player.y = player_pos
            self.game.player.angle = player_rot
            print(f"PLAYER SPAWN SET: {player_pos}, ROTATION: {player_rot}")
        if sky_name:
            self.game.object_renderer.load_sky_texture(sky_name)
            print(f"LOADED SKY TEXTURE: {sky_name}")

        print("Level loaded!")
