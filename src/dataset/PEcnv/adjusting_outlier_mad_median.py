import numpy as np

from pynguin.dataset.PEcnv import measures


def outlier_mad_median(a):
    K = 2.24
    a = np.asarray(a)
    dists = np.abs(a - np.median(a))
    mad = measures.median_absolute_deviation(a)
    return dists / mad > K
