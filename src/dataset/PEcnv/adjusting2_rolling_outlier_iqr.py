import numpy as np

from pynguin.dataset.PEcnv.adjusting2 import savgol, rolling_quantile


def rolling_outlier_iqr(x, width, c=3.0):
    if len(x) <= width:
        return np.zeros(len(x), dtype=np.bool_)
    dists = x - savgol(x, width)
    q_hi = rolling_quantile(dists, width, 0.75)
    q_lo = rolling_quantile(dists, width, 0.25)
    iqr = q_hi - q_lo
    outliers = np.abs(dists) > iqr * c
    return outliers
