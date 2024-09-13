from __future__ import absolute_import, print_function, division
import numpy as np

from pynguin.dataset.cnvpytor import betapdf


def beta_overlap(rc1, rc2, dx=0.001):
    """
    Returns approximative overlap area of two beta functions.

    Parameters
    ----------
    rc1 : pair of int
        First beta counts
    rc2 : pair of int
        Second beta counts

    Returns
    -------
    overlap : float
        Overlap area.

    """
    x = np.arange(0, 1.0 + dx, dx)
    f1 = betapdf(x, *rc1)
    f2 = betapdf(x, *rc2)
    r = np.sum(f1 * f2) / (np.sum(f1) * np.sum(f2))
    return np.sqrt(r) if r < 1.0 else 1.0
