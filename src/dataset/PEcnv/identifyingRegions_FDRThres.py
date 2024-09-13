from __future__ import division
import logging
import numpy as np
from scipy import stats

def FDRThres(x, q, stdev):
    """False discovery rate (FDR) threshold."""
    M = len(x)
    if M < 2:
        return 0
    m = np.arange(1, M + 1) / M
    x_sorted = np.sort(np.abs(x))[::-1]
    p = 2 * (1 - stats.norm.cdf(x_sorted, stdev))
    indices = np.nonzero(p <= m * q)[0]
    if len(indices):
        T = x_sorted[indices[-1]]
    else:
        logging.debug('No passing p-values: min p=%.4g, min m=%.4g, q=%s', p[0], m[0], q)
        T = x_sorted[0] + 1e-16
    return T
