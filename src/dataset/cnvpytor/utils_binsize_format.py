from __future__ import absolute_import, print_function, division


def binsize_format(x):
    """
    Converts integer to human readable format (K - x1000, M - x1e6)

    Parameters
    ----------
    x : int

    Returns
    -------
    sx : str

    """
    if x >= 1000000:
        return str(x // 1000000) + 'M'
    elif x >= 1000:
        return str(x // 1000) + 'K'
    else:
        return str(x)
