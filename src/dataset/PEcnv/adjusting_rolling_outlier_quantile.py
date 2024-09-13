import numpy as np

from pynguin.dataset.PEcnv.adjusting import rolling_quantile, savgol


def rolling_outlier_quantile(x, width, q, m):
    if len(x) <= width:
        return np.zeros(len(x), dtype=np.bool_)
    dists = np.abs(x - savgol(x, width))
    quants = rolling_quantile(dists, width, q)
    outliers = dists > quants * m
    return outliers
