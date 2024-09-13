from __future__ import absolute_import, print_function, division

from pynguin.dataset.cnvpytor import decode_position


def decode_region(s, max_size=1000000000):
    """

    Parameters
    ----------
    s : str

    Returns
    -------
    list of tuples

    """
    regs = s.split(',')
    ret = []
    for r in regs:
        chr_interval = r.split(':')
        if len(chr_interval) > 1:
            begin_end = chr_interval[1].split('-')
            ret.append((chr_interval[0], (decode_position(begin_end[0]), decode_position(begin_end[1]))))
        else:
            ret.append((chr_interval[0], (1, max_size)))
    return ret
