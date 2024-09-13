
import numpy as np

from pynguin.dataset.PEcnv.measures import on_weighted_array


@on_weighted_array()
def weighted_std(a, weights):
    mean = np.average(a, weights=weights)
    var = np.average((a - mean) ** 2, weights=weights)
    return np.sqrt(var)
