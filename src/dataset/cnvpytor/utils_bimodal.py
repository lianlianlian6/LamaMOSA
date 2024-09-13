from __future__ import absolute_import, print_function, division

from pynguin.dataset.cnvpytor import normal


def bimodal(x, a1, x01, sigma1, a2, x02, sigma2):
    return normal(x, a1, x01, sigma1) + normal(x, a2, x02, sigma2)
