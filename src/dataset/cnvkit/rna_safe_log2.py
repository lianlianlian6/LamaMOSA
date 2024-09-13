import numpy as np
def safe_log2(values, min_log2):
    """Transform values to log2 scale, safely handling zeros.

    Parameters
    ----------
    values : np.array
        Absolute-scale values to transform. Should be non-negative.
    min_log2 : float
        Assign input zeros this log2-scaled value instead of -inf. Rather than
        hard-clipping, input values near 0 (especially below 2^min_log2) will be
        squeezed a bit above `min_log2` in the log2-scale output.
    """
    absolute_shift = 2 ** min_log2
    return np.log2(values + absolute_shift)
