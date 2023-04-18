from map import Map
from renderer.sprite_object import SpriteObject, AnimatedSpriteObject
from renderer.object_renderer import ObjectRenderer
from renderer.objects_manager import OBJECTS


MAP_START = "map start"
MAP_END = "map end"
OBJECT = "object "
OBJECT_END = "object end"


class Level:
    def __init__(self, path: str, game) -> None:
        self.path: str = path
        self.game = game
        self.objects_manager = game.objects_manager

        self.map: Map = Map()
        self.sprite_objects: list[SpriteObject] = []

        self.load()
    
    def load(self) -> None:
        print("Loaded wall texture keys:", ObjectRenderer.WALL_TEXTURES_KEYS)

        with open(self.path, "r") as f:
            lines = f.read().split("\n")
        
        map_start = False
        map_end = False
        map = []

        object_name = None

        for lineno, line in enumerate(lines):
            print("Read:", line)

            if len(line) == 0 or line.startswith("#"):
                continue

            if line == MAP_START:
                if map_start:
                    raise Exception("Cannot define a second map start!")

                map_start = True
                continue

            if line == MAP_END:
                if map_end:
                    raise Exception("Cannot define a second map end!")

                map_end = True
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

            if object_name:
                obj_x, obj_y = line.split()
                obj_x, obj_y = float(obj_x), float(obj_y)
                try:
                    if map[int(obj_y)][int(obj_x)] != " ":
                        print(f"\nWARN: {object_name} at {obj_x, obj_y} is in a wall!\n")
                except IndexError:
                    pass
                self.objects_manager.add_sprite(OBJECTS[object_name].make_at_position(self.game, (float(obj_x), float(obj_y))))

            if map_start and not map_end:  # started reading the map but didn't stop yet
                map_row = []
                for c in line.strip():
                    if c == " ":
                        map_row.append(" ")
                    elif c in ObjectRenderer.WALL_TEXTURES_KEYS:
                        map_row.append(c)
                    else:
                        raise Exception(f"Unknown map cell type '{c}'!")
                map.append(map_row)
                continue
        
        if not map_start or not map_end:
            raise Exception("Cannot find 'map start' or 'map end'!")
        
        if object_name:
            raise Exception("Object definition did not end!")
        
        self.map.load(map)

        print("Level loaded!")
