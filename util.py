import math


def clamp_min(value, min_v):
    return max(value, min_v)


def clamp_max(value, max_v):
    return min(value, max_v)


def clamp(value, min_v, max_v):
    return clamp_max(clamp_min(value, min_v), max_v)


def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)
