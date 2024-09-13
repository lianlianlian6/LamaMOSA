import numpy as np

from pynguin.dataset.PEcnv.adjusting2 import guess_window_size, check_inputs, convolve_unweighted, convolve_weighted, \
    _fit_edges


def kaiser(x, width=None, weights=None, do_fit_edges=False):
    if len(x) < 2:
        return x
    if width is None:
        width = guess_window_size(x, weights)
    (x, wing, *padded) = check_inputs(x, width, False, weights)
    window = np.kaiser(2 * wing + 1, 14)
    if weights is None:
        (signal,) = padded
        y = convolve_unweighted(window, signal, wing)
    else:
        (signal, weights) = padded
        (y, _w) = convolve_weighted(window, signal, weights)
    if do_fit_edges:
        _fit_edges(x, y, wing)
    return y
