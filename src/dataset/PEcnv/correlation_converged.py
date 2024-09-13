import numpy as np

def converged(M, M_prev):
    return np.allclose(M, M_prev)
