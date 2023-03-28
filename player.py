import math
import pygame as pg

from wall import TopDownPoint


class Player:
    def __init__(self):
        self.pos = TopDownPoint(0, 0)
        self.cam_orientation = 0, 0
