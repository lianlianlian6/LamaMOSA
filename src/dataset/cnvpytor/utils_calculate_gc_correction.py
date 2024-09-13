from __future__ import absolute_import, print_function, division
import numpy as np

def calculate_gc_correction(his_rd_gc, mean, sigma, bin_size=1, gc_corr_rm_ol=False):
    """ Calculate GC correction from RD-GC histogram
    """
    min_bin = 1
    max_bin = min(int(max(2 * mean, mean + 5 * sigma) / bin_size), his_rd_gc.shape[0])
    if gc_corr_rm_ol:
        min_bin = int(0.75 * mean / bin_size)
        max_bin = min(int(1.25 * mean / bin_size), his_rd_gc.shape[0])
    his = his_rd_gc[min_bin:max_bin, :]
    rd = np.repeat(np.arange(min_bin * bin_size, max_bin * bin_size, bin_size).reshape((max_bin - min_bin, 1)), 101, axis=1)
    np.seterr(divide='ignore', invalid='ignore')
    gc_corr = np.sum(rd * his, axis=0) / np.sum(his, axis=0)
    no_stat = np.isnan(gc_corr)
    gc_corr[no_stat] = 1
    gc_corr = gc_corr / (np.sum(gc_corr * np.sum(his, axis=0)) / np.sum(np.sum(his, axis=0)))
    gc_corr[no_stat] = 1
    return gc_corr
