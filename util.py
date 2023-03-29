def clamp_min(value, min_v):
    return max(value, min_v)


def clamp_max(value, max_v):
    return min(value, max_v)


def clamp(value, min_v, max_v):
    return clamp_max(clamp_min(value, min_v), max_v)
