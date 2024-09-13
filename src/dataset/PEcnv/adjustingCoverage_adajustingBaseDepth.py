import numpy as np

from pynguin.dataset.PEcnv.adjustingCoverage import adajustedEdge

a = 2 / 10
def adajustingBaseDepth(index, raw_depth, n1, n2):
    limit2 = len(raw_depth) - (index + n2 + 1)
    adjusted_depth = raw_depth[index]
    if len(raw_depth) < n1 or len(raw_depth) < n2:
        raise ValueError('n1 or n2 given must be less than len of the sequence.')
    if index <= n1:
        adjusted_depth = adajustedEdge(index, raw_depth)
    elif limit2 <= 0:
        front_bases = raw_depth[n1:index + 1]
        around_avg = np.mean(front_bases)
        adjusted_depth = (1 - a) * adajustingBaseDepth(index - 1, raw_depth, n1, n2) + a * around_avg
    else:
        around_bases = raw_depth[index + n1:index + n2 + 1]
        around_avg = np.mean(around_bases)
        adjusted_depth = (1 - a) * adajustingBaseDepth(index - 1, raw_depth, n1, n2) + a * around_avg
    return adjusted_depth
