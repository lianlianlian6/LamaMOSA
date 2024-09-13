from __future__ import absolute_import, print_function, division
from scipy.stats import beta


def betapdf(x, a, b):
    return beta.pdf(x, a + 1, b + 1)
