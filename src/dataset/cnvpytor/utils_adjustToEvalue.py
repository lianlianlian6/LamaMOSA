from __future__ import absolute_import, print_function, division
from pynguin.dataset.cnvpytor import getEValue


def adjustToEvalue(mean, sigma, rd, start, end, pval, max_steps=1000):
    val = getEValue(mean, sigma, rd, start, end)
    step = 0
    done = False
    while val > pval and (not done) and (step < max_steps):
        done = True
        step += 1
        (v1, v2, v3, v4) = (10000000000.0, 10000000000.0, 10000000000.0, 10000000000.0)
        if start > 0:
            v1 = getEValue(mean, sigma, rd, start - 1, end)
        if end - start > 2:
            v2 = getEValue(mean, sigma, rd, start + 1, end)
            v3 = getEValue(mean, sigma, rd, start, end - 1)
        if end < len(rd):
            v4 = getEValue(mean, sigma, rd, start, end + 1)
        if min(v1, v2, v3, v4) < val:
            done = False
            if v1 == min(v1, v2, v3, v4):
                start -= 1
                val = v1
            elif v2 == min(v1, v2, v3, v4):
                start += 1
                val = v2
            elif v3 == min(v1, v2, v3, v4):
                end -= 1
                val = v3
            elif v4 == min(v1, v2, v3, v4):
                end += 1
                val = v4
    if val <= pval:
        return (start, end)
    return None
