from __future__ import absolute_import, print_function, division
import numpy as np

def gc_at_compress(gc, at):
    """
    Compress GC/AT content of 100bins using fact that #at+#gc=100 in large majority of bins.
    Transforms #at, #gc -> #at, 100-#at-#gc

    Parameters
    ----------
    gc : list of int
        Binned GC content (100bp bins).
    at : list of int
        Binned AT content (100bp bins).

    Returns
    -------
    gcat : numpy.ndarray
        Array contains compressed GC/AT content.

    """
    cgc = np.array(gc)
    cat = 100 - np.array(at) - cgc
    return np.concatenate((cgc, cat)).astype('uint8')
