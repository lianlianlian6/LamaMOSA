from __future__ import division
import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.identifyingRegions import indentifyingRegions, break_points_merge, haarSeg


def PE_haar(I, breaksFdrQ, W=None, rawI=None, haarStartLevel=1, haarEndLevel=5):
    if len(I) > 1:
        seq_data_arr = pd.DataFrame(I)
        segs = indentifyingRegions(seq_data_arr)
        breakPoints = break_points_merge(segs, I, breaksFdrQ, W, rawI, haarStartLevel, haarEndLevel)
        if breakPoints['start'].size == 0:
            try:
                breakPoints = haarSeg(I, breaksFdrQ, W, rawI, haarStartLevel, haarEndLevel)
            except:
                breakPoints = {'start': np.array([0]), 'end': np.array([1]), 'size': np.array([2]), 'mean': np.array([0])}
    else:
        try:
            breakPoints = haarSeg(I, breaksFdrQ, W, rawI, haarStartLevel, haarEndLevel)
        except:
            breakPoints = {'start': np.array([0]), 'end': np.array([1]), 'size': np.array([2]), 'mean': np.array([0])}
    return breakPoints
