import numpy as np
from pynguin.dataset.PEcnv import measures

def outlier_iqr(a, c=3.0):
    a = np.asarray(a)
    dists = np.abs(a - np.median(a))
    iqr = measures.interquartile_range(a)
    return dists > c * iqr
