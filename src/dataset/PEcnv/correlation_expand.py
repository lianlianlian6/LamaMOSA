import numpy as np

def expand(A, expansion):
    return np.linalg.matrix_power(A, expansion)
