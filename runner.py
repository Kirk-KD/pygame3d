import os
import time

try:
    import pathfinding, pygame, PIL  # all needed libraries
except ModuleNotFoundError:
    print("Missing libraries, installing...")
    os.system("py -m pip install -r requirements.txt")  # install from requirements
    print("Finished installing, running the game now...")

    time.sleep(0.5)  # wait for libraries to update in case computer is slow

os.system("py DOOM/main.py")  # run the game
