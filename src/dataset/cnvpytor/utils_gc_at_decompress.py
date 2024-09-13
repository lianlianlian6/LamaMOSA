from __future__ import absolute_import, print_function, division

def gc_at_decompress(gcat):
    """
    Decompress GT/AC content - inverse function of gc_at_compress(gc, at).

    Parameters
    ----------
    gcat : numpy.ndarray
        Array contains compressed GC/AT content.

    Returns
    -------
    gc : list of int
        Binned GC content (100bp bins).
    at : list of int
        Binned AT content (100bp bins).

    """
    return (list(map(int, gcat[:gcat.size // 2])), list(map(int, 100 - gcat[:gcat.size // 2] - gcat[gcat.size // 2:])))
