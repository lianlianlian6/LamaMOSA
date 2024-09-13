from __future__ import absolute_import, print_function, division
import numpy as np

def gcp_decompress(gcat, bin_ratio=1):
    """
    Decompress GT/AC content and calculate GC percentage.

    Parameters
    ----------
    gcat : numpy.ndarray
        Array contains compressed GC/AT content.

    Returns
    -------
    gcp : list of int
        GC percentage.

    """
    (gc, at) = (gcat[:gcat.size // 2].astype('float'), (100 - gcat[:gcat.size // 2] - gcat[gcat.size // 2:]).astype('float'))
    if bin_ratio == 1:
        return 100.0 * gc / (at + gc + 1e-10)
    n = len(gc)
    his_gc = np.concatenate((np.array(gc), np.zeros(bin_ratio - n + n // bin_ratio * bin_ratio))).astype('float')
    his_gc.resize((len(his_gc) // bin_ratio, bin_ratio))
    his_gc = his_gc.sum(axis=1)
    his_at = np.concatenate((np.array(at), np.zeros(bin_ratio - n + n // bin_ratio * bin_ratio))).astype('float')
    his_at.resize((len(his_at) // bin_ratio, bin_ratio))
    his_at = his_at.sum(axis=1)
    return 100.0 * his_gc / (his_at + his_gc + 1e-10)
