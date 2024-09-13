import numpy as np

def _pad_array(x, wing):
    return np.concatenate((x[wing - 1::-1], x, x[:-wing - 1:-1]))
