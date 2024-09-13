from __future__ import absolute_import, print_function, division
import numpy as np

from pynguin.dataset.cnvpytor import t_test_1_sample


def getEValue(mean, sigma, rd, start, end):
    aver = np.nanmean(rd[start:end])
    s = np.nanstd(rd[start:end])
    if s == 0:
        s = sigma * aver / mean if sigma > 0 else 1
    return t_test_1_sample(mean, aver, s, end - start) / (end - start)
