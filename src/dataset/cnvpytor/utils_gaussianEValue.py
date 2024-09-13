from __future__ import absolute_import, print_function, division
import numpy as np
from scipy.special import erf

def gaussianEValue(mean, sigma, rd, start, end):
    aver = np.nanmean(rd[start:end])
    max = np.nanmax(rd[start:end])
    min = np.nanmin(rd[start:end])
    if aver < mean:
        x = (max - mean) / (sigma * np.sqrt(2.0))
        return np.power(0.5 * (1.0 + erf(x)), end - start)
    x = (min - mean) / (sigma * np.sqrt(2.0))
    return np.power(0.5 * (1.0 - erf(x)), end - start)
