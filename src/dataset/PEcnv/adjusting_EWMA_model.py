import math
import numpy as np

from pynguin.dataset.PEcnv.adjusting import breakpoint_select


def EWMA_model(arr):
    sp0 = 9
    mu0 = arr.mean()
    num0 = float(2 / (1 + sp0))
    std0 = arr.std()
    upline0 = mu0 + std0 * 3 * math.sqrt(num0 / (2 - num0))
    dowline0 = mu0 - std0 * 3 * math.sqrt(num0 / (2 - num0))
    breakpointSelects0 = breakpoint_select(arr, sp0, upline0, dowline0)
    arr_ = arr.iloc[::-1]
    sp1 = 9
    num1 = float(2 / (1 + sp1))
    mu1 = arr_.mean()
    num1 = float(2 / (1 + sp1))
    std1 = arr_.std()
    upline1 = mu1 + std1 * 3 * math.sqrt(num1 / (2 - num1))
    dowline1 = mu1 - std1 * 3 * math.sqrt(num1 / (2 - num1))
    breakpointSelects1 = breakpoint_select(arr_, sp1, upline1, dowline1)
    breakpointSelects2 = []
    for r in breakpointSelects1[::-1]:
        breakpointSelects2.append(np.abs(r - (len(arr) - 1)))
    breakpointSelects = sorted(list(set(breakpointSelects0 + breakpointSelects2)))
    if len(breakpointSelects) > 0:
        segs = EWMA_SEG(breakpointSelects)
        return segs
    else:
        return [[0, len(arr) - 1]]
