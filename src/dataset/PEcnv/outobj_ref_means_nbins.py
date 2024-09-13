import logging
import numpy as np

def ref_means_nbins(tumor_segs, normal_cn):
    if normal_cn:
        log2s_in_segs = [bins['log2'] for (_seg, bins) in normal_cn.by_ranges(tumor_segs)]
        ref_means = np.array([s.mean() for s in log2s_in_segs])
        if 'probes' in tumor_segs:
            nbins = tumor_segs['probes']
        else:
            nbins = np.array([len(s) for s in log2s_in_segs])
    else:
        ref_means = np.zeros(len(tumor_segs))
        if 'weight' in tumor_segs and (tumor_segs['weight'] > 1.0).any():
            nbins = tumor_segs['weight']
            nbins /= nbins.max() / nbins.mean()
        else:
            if 'probes' in tumor_segs:
                nbins = tumor_segs['probes']
            else:
                logging.warning('No probe counts in tumor segments file and no normal reference given; guessing normal read-counts-per-segment from segment sizes')
                sizes = tumor_segs.end - tumor_segs.start
                nbins = sizes / sizes.mean()
            if 'weight' in tumor_segs:
                nbins *= tumor_segs['weight'] / tumor_segs['weight'].mean()
    return (ref_means, nbins)
