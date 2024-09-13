import numpy as np

from pynguin.dataset.PEcnv.adjusting import savgol, rolling_std


def rolling_outlier_std(x, width, stdevs):
    if len(x) <= width:
        return np.zeros(len(x), dtype=np.bool_)
    dists = x - savgol(x, width)
    x_std = rolling_std(dists, width)
    outliers = np.abs(dists) > x_std * stdevs
    return outliers
