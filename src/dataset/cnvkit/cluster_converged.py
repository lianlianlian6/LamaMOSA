import logging
import numpy as np

def converged(M, M_prev):
    """Test convergence.

    Criterion: homogeneity(??) or no change from previous round.
    """
    return np.allclose(M, M_prev)