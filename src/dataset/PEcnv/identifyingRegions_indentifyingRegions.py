from __future__ import division
import math
import numpy as np

from pynguin.dataset.PEcnv.identifyingRegions import breakpoint_select, selectingSegments


def indentifyingRegions(arr):
    mu0 = arr[0].mean()
    num0 = 0.2
    std0 = arr[0].std()
    upline0 = mu0 + std0 * 3 * math.sqrt(num0 / (2 - num0))
    dowline0 = mu0 - std0 * 3 * math.sqrt(num0 / (2 - num0))
    breakpointSelects0 = breakpoint_select(arr, upline0, dowline0)
    arr_ = arr.iloc[::-1]
    mu1 = arr_[0].mean()
    num1 = 0.2
    std1 = arr_[0].std()
    upline1 = mu1 + std1 * 3 * math.sqrt(num1 / (2 - num1))
    dowline1 = mu1 - std1 * 3 * math.sqrt(num1 / (2 - num1))
    breakpointSelects1 = breakpoint_select(arr_, upline1, dowline1)
    breakpointSelects2 = []
    for r in breakpointSelects1[::-1]:
        breakpointSelects2.append(np.abs(r - (len(arr) - 1)))
    breakpointSelects = sorted(list(set(breakpointSelects0 + breakpointSelects2)))
    if len(breakpointSelects) > 0:
        segs = selectingSegments(breakpointSelects)
        return segs
    else:
        return [[0, len(arr) - 1]]
