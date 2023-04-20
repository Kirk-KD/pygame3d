import math
from map import Map
from png_map import PNGMap
from renderer.sprite_object import SpriteObject, AnimatedSpriteObject
from renderer.object_renderer import ObjectRenderer
from renderer.objects_manager import OBJECTS
from enemy import ENEMIES


OBJECT = "object "
OBJECT_END = "object end"
ENEMY = "enemy "
ENEMY_END = "enemy end"
PLAYER = "player "


class Level:
    def __init__(self, path: str, game) -> None:
        self.path: str = path
        self.game = game
        self.objects_manager = game.objects_manager

        self.png_map: PNGMap = PNGMap(self.path + ".png")
        self.map: Map = Map()
        self.sprite_objects: list[SpriteObject] = []

        self.load()
    
    def load(self) -> None:
        print("Loaded wall texture keys:", ObjectRenderer.WALL_TEXTURES_KEYS)

        with open(self.path + ".txt", "r") as f:
            lines = f.read().split("\n")

        object_name = None
        enemy_name = None

        player_pos = None

        for lineno, line in enumerate(lines):
            print("Read:", line)

            if len(line) == 0 or line.startswith("#"):
                continue

            if line == OBJECT_END:
                if object_name is None:
                    raise Exception("No object definition to end!")

                object_name = None
                continue

            if line.startswith(OBJECT):
                object_name = line[len(OBJECT):]
                if object_name not in OBJECTS:
                    raise Exception(f"No object named '{object_name}' found!")
                continue
                
            if line.startswith(PLAYER):
                if player_pos is not None:
                    raise Exception("Cannot define player spawn pos twice!")
                p = line[len(PLAYER):].split()
                player_pos = float(p[0]), float(p[1])
                player_rot = math.radians(float(p[2]) + 85)
                continue

            if object_name:
                obj_x, obj_y = line.strip().split()
                obj_x, obj_y = float(obj_x), float(obj_y)
                self.objects_manager.add_sprite(OBJECTS[object_name].make_at_position(self.game, (float(obj_x), float(obj_y))))
                continue

            if line == ENEMY_END:
                enemy_name = None
                continue

            if line.startswith(ENEMY):
                if enemy_name is not None:
                    raise Exception(f"Didn't end enemy def!")

                enemy_name = line[len(ENEMY):]
                if enemy_name not in ENEMIES:
                    raise Exception(f"No enemy named '{enemy_name}'!")
                
                continue

            if enemy_name:
                enemy_x, enemy_y = line.strip().split()
                enemy_x, enemy_y = float(enemy_x), float(enemy_y)
                self.objects_manager.add_enemy(ENEMIES[enemy_name](self.game, (enemy_x, enemy_y)))
                continue
        
        if object_name:
            raise Exception("Object definition did not end!")
        
        # self.map.load(map)
        self.map.load(self.png_map.to_map())
        if player_pos:
            self.game.player.x, self.game.player.y = player_pos
            self.game.player.angle = player_rot
            print(f"PLAYER SPAWN SET: {player_pos}, ROTATION: {player_rot}")

        print("Level loaded!")
