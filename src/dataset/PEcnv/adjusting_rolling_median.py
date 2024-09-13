import numpy as np

from pynguin.dataset.PEcnv.adjusting import EWMA_model, merge_segs, check_inputs


def rolling_median(x, width):
    seq_data_arr = x
    segs = EWMA_model(seq_data_arr)
    newSegs = merge_segs(segs)
    interm = 0
    tmPos = 0
    winSize = 2
    if len(newSegs) > 0:
        for seg in newSegs:
            'Rolling median with mirrored edges.'
            seg_x = x[seg[0]:seg[1]]
            if seg_x.size > winSize + 1:
                (seg_x, wing, signal) = check_inputs(seg_x, width)
                seg_rolled = signal.rolling(2 * wing + 1, 1, center=True).median()
                seg_rolled = np.asfarray(seg_rolled[wing:-wing])
                seg_rolled_toli = seg_rolled.tolist()
            else:
                seg_rolled_toli = seg_x.tolist()
            normal_x = x[tmPos:seg[0]]
            tmPos = seg[1]
            if normal_x.size > winSize + 1:
                (normal_x, wing, signal) = check_inputs(normal_x, width)
                rolled = signal.rolling(winSize * wing + 1, 1, center=True).median()
                rolled = np.asfarray(rolled[wing:-wing])
                rolled_toli = rolled.tolist()
                rolled_toli = rolled_toli + seg_rolled_toli
                if interm == 0:
                    rolledAll = rolled_toli
                    interm += 1
                else:
                    rolledAll += rolled_toli
            else:
                rolled_toli = normal_x.tolist()
                rolled_toli = rolled_toli + seg_rolled_toli
                if interm == 0:
                    rolledAll = rolled_toli
                    interm += 1
                else:
                    rolledAll += rolled_toli
        if tmPos != x[x.size - 1]:
            endList = x[tmPos:]
            if endList.size > winSize + 1:
                (endList, wing, signal) = check_inputs(endList, width)
                rolled = signal.rolling(winSize * wing + 1, 1, center=True).median()
                rolled = np.asfarray(rolled[wing:-wing])
                rolled_toli = rolled.tolist()
                if interm == 0:
                    rolledAll = rolled_toli
                    interm += 1
                else:
                    rolledAll += rolled_toli
            else:
                endList = endList.tolist()
                rolled_toli = endList
                if interm == 0:
                    rolledAll = rolled_toli
                    interm += 1
                else:
                    rolledAll += rolled_toli
        rolledAll_ = np.asfarray(rolledAll)
    else:
        'Rolling median with mirrored edges.'
        (x, wing, signal) = check_inputs(x, width)
        rolled = signal.rolling(winSize * wing + 1, 1, center=True).median()
        rolledAll_ = np.asfarray(rolled[wing:-wing])
    return rolledAll_
