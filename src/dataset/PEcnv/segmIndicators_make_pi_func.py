import numpy as np

def make_pi_func(alpha):
    pct_lo = 100 * alpha / 2
    pct_hi = 100 * (1 - alpha / 2)

    def pi_func(ser, _w):
        return np.percentile(ser, [pct_lo, pct_hi])
    return pi_func
