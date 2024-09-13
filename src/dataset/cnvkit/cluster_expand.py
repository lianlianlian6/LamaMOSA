import logging
import numpy as np

def expand(A, expansion):
    """Apply cluster expansion with the given matrix power."""
    return np.linalg.matrix_power(A, expansion)