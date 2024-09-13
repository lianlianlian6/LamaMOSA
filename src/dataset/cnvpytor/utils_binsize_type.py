from __future__ import absolute_import, print_function, division
from argparse import ArgumentTypeError


def binsize_type(x):
    """
    Casts to int and checks divisibility by 100 (native bin size).

    Parameters
    ----------
    x : int, str or float
        Bin size

    Returns
    -------
    : int
        Bin size

    """
    x = int(x)
    if x % 100 != 0 or x <= 0:
        raise ArgumentTypeError('Bin size should be positive integer divisible by 100!')
    return x
