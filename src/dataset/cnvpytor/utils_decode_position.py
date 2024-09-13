from __future__ import absolute_import, print_function, division


def decode_position(s):
    """

    Parameters
    ----------
    s : str

    Returns
    -------
    str
    """
    return int(s.replace('K', '000').replace('k', '000').replace('M', '000000').replace('m', '000000'))
