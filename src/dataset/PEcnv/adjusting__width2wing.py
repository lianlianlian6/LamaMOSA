import math

def _width2wing(width, x, min_wing=3):
    if 0 < width < 1:
        wing = int(math.ceil(len(x) * width * 0.5))
    elif width >= 2 and int(width) == width:
        width = min(width, len(x) - 1)
        wing = int(width // 2)
    else:
        raise ValueError('width must be either a fraction between 0 and 1 or an integer greater than 1 (got %s)' % width)
    wing = max(wing, min_wing)
    wing = min(wing, len(x) - 1)
    assert wing >= 1, 'Wing must be at least 1 (got %s)' % wing
    return wing
