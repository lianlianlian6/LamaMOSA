import math

def cvg2rgb(cvg, desaturate):
    cutoff = 1.33
    x = min(abs(cvg) / cutoff, 1.0)
    if desaturate:
        x = ((1.0 - math.cos(x * math.pi)) / 2.0) ** 0.8
        s = x ** 1.2
    else:
        s = x
    if cvg < 0:
        rgb = (1 - s, 1 - s, 1 - 0.25 * x)
    else:
        rgb = (1 - 0.25 * x, 1 - s, 1 - s)
    return rgb
