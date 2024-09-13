import numpy as np
from pynguin.dataset.PEcnv import measures

def ests_of_scale(deviations):
    std = np.std(deviations, dtype=np.float64)
    mad = measures.median_absolute_deviation(deviations)
    iqr = measures.interquartile_range(deviations)
    biw = measures.biweight_midvariance(deviations)
    return (std, mad, iqr, biw)
