import numpy as np

from pynguin.dataset.PEcnv.measures import on_weighted_array, weighted_median


@on_weighted_array()
def weighted_mad(a, weights, scale_to_sd=True):
    a_median = weighted_median(a, weights)
    mad = weighted_median(np.abs(a - a_median), weights)
    if scale_to_sd:
        mad *= 1.4826
    return mad
