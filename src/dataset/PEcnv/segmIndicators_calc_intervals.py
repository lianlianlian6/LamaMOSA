import numpy as np

def calc_intervals(bins_log2s, weights, func):
    out_vals_lo = np.repeat(np.nan, len(bins_log2s))
    out_vals_hi = np.repeat(np.nan, len(bins_log2s))
    for (i, ser) in enumerate(bins_log2s):
        if len(ser):
            wt = weights[ser.index]
            assert (wt.index == ser.index).all()
            (out_vals_lo[i], out_vals_hi[i]) = func(ser.values, wt.values)
    return (out_vals_lo, out_vals_hi)
