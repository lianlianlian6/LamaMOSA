import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.adjusting2 import EWMA_model, check_inputs


def rolling_median(x, width):
    seq_data_arr = x
    segs = EWMA_model(seq_data_arr)
    interm = 0
    if len(segs) > 0:
        for seg in segs:
            'Rolling median with mirrored edges.'
            seg_x = x[seg[0]:seg[1]]
            seg_x = seg_x.tolist()
            normal_x = np.concatenate((x[:seg[0]], x[seg[1]:]))
            if len(normal_x) > 3:
                (normal_x, wing, signal) = check_inputs(normal_x, width)
                rolled = signal.rolling(20 * wing + 1, 1, center=True).median()
                rolled = np.asfarray(rolled[wing:-wing])
                rolled_toli = rolled.tolist()
                rolled_toli[seg[0]:seg[0]] = iter(seg_x)
                if interm == 0:
                    rolledAll = pd.Series(rolled_toli)
                    interm += 1
                else:
                    rolledAll += pd.Series(rolled_toli)
            else:
                rolled_toli = normal_x.tolist()
                rolled_toli[seg[0]:seg[0]] = iter(seg_x)
                if interm == 0:
                    rolledAll = pd.Series(rolled_toli)
                    interm += 1
                else:
                    rolledAll += pd.Series(rolled_toli)
        rolledAll_ = rolledAll / len(segs)
    else:
        'Rolling median with mirrored edges.'
        (x, wing, signal) = check_inputs(x, width)
        rolled = signal.rolling(20 * wing + 1, 1, center=True).median()
        rolledAll_ = np.asfarray(rolled[wing:-wing])
    return rolledAll_
