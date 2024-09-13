from __future__ import division
import numpy as np

def SegmentByPeaks(data, peaks, weights=None):
    segs = np.zeros_like(data)
    for (seg_start, seg_end) in zip(np.insert(peaks, 0, 0), np.append(peaks, len(data))):
        if weights is not None and weights[seg_start:seg_end].sum() > 0:
            val = np.average(data[seg_start:seg_end], weights=weights[seg_start:seg_end])
        else:
            val = np.mean(data[seg_start:seg_end])
        segs[seg_start:seg_end] = val
    return segs
