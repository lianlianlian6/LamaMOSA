import numpy as np
from scipy.stats import norm

from pynguin.dataset.PEcnv.prebin import p_adjust_bh


def z_prob(cnarr):
    sd = np.sqrt(1 - cnarr['weight'])
    z = cnarr['log2'] / sd
    p = 2.0 * norm.cdf(-np.abs(z))
    return p_adjust_bh(p)
