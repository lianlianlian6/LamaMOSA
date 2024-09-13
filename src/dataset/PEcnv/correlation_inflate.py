import numpy as np

from pynguin.dataset.PEcnv.correlation import normalize


def inflate(A, inflation):
    return normalize(np.power(A, inflation))
