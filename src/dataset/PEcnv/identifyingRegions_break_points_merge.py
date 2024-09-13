from __future__ import division
import numpy as np
import pandas as pd
from matplotlib import pyplot

from pynguin.dataset.PEcnv.identifyingRegions import haarSeg, sort_breakpoints


def break_points_merge(segs, I, breaksFdrQ, W, rawI, haarStartLevel, haarEndLevel):
    index_seg = 0
    dict2 = {}
    start = []
    end = []
    size = []
    mean = []
    end_index = 0
    seq_data_arr = pd.DataFrame(I)
    adjusted_data = seq_data_arr
    I0 = np.array(adjusted_data)
    indices = np.arange(len(I0))
    pyplot.scatter(indices, adjusted_data, alpha=0.2, c='r')
    for seg in segs:
        seg_table = haarSeg(I0[seg[0]:seg[1]], breaksFdrQ)
        start0 = []
        end0 = []
        size0 = []
        mean0 = []
        if seg_table['start'].size < 2:
            continue
        if seg_table['start'].size == 3 or seg_table['start'].size == 2:
            for i in range(seg_table['start'].size):
                seg_table['end'][i] += seg[0]
                seg_table['start'][i] += seg[0]
                start0.append(seg_table['start'][i])
                end0.append(seg_table['end'][i])
                size0.append(seg_table['size'][i])
            if seg_table['start'].size == 3:
                if index_seg == 0:
                    mean0 = seg_table['mean'].tolist()
                    index_seg += 1
                else:
                    mean0 = seg_table['mean'][1:].tolist()
            else:
                mean0 = seg_table['mean'].tolist()
        if seg_table['start'].size == 2:
            if abs(seg_table['start'][-1] - seg[0]) >= abs(seg_table['start'][-1] - seg[-1]):
                start0.insert(0, seg[0] - 2)
                end0.insert(0, seg[0] - 1)
                size0.insert(0, 2)
                if index_seg == 0:
                    mean0.insert(0, seg_table['mean'][0])
                    index_seg += 1
            else:
                start0.append(seg[-1])
                end0.append(seg[-1] + 2)
                size0.append(3)
                if index_seg == 0:
                    mean0.append(seg_table['mean'][-1])
                    index_seg += 1
        start += start0[1:]
        end += end0[:-1]
        mean += mean0
        for i in range(1, len(start)):
            for j in range(0, len(start) - i):
                if start[j] > start[j + 1]:
                    (start[j], start[j + 1]) = (start[j + 1], start[j])
                    (mean[j], mean[j + 1]) = (mean[j + 1], mean[j])
                    (end[j], end[j + 1]) = (end[j + 1], end[j])
    if len(start) > 0:
        start.insert(0, 0)
        end.append(len(I) - 1)
        size = list(map(lambda x, y: x - y + 1, end, start))
    else:
        dict2['start'] = np.array(start)
        dict2['end'] = np.array(end)
        dict2['size'] = np.array(size)
        dict2['mean'] = np.array(mean)
        return dict2
    if end[0] <= 0:
        del end[0]
        del start[0]
        del mean[0]
        del size[0]
    if start[-1] >= len(I) - 1:
        del end[-1]
        del start[-1]
        del mean[-1]
        del size[-1]
    dict2['start'] = np.array(start)
    dict2['end'] = np.array(end)
    dict2['size'] = np.array(size)
    newdict = sort_breakpoints(dict2)
    means = []
    for i in range(len(newdict['start'])):
        means.append(np.mean(I[newdict['start'][i]:newdict['end'][i]]))
    newdict['mean'] = np.array(means)
    return newdict
