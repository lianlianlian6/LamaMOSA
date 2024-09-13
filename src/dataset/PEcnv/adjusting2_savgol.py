import logging
from scipy.signal import savgol_coeffs, savgol_filter

from pynguin.dataset.PEcnv.adjusting2 import check_inputs, convolve_weighted


def savgol(x, total_width=None, weights=None, window_width=7, order=3, n_iter=1):
    if len(x) < 2:
        return x
    if total_width:
        n_iter = max(1, min(1000, total_width // window_width))
    else:
        total_width = n_iter * window_width
    logging.debug('adjusting in %d iterations for effective bandwidth %d', n_iter, total_width)
    if weights is None:
        (x, total_wing, signal) = check_inputs(x, total_width, False)
        y = signal
        for _i in range(n_iter):
            y = savgol_filter(y, window_width, order, mode='interp')
    else:
        (x, total_wing, signal, weights) = check_inputs(x, total_width, False, weights)
        window = savgol_coeffs(window_width, order)
        (y, w) = convolve_weighted(window, signal, weights, n_iter)
    bad_idx = (y > x.max()) | (y < x.min())
    if bad_idx.any():
        logging.warning('adjusting overshot at {} / {} indices: ({}, {}) vs. original ({}, {})'.format(bad_idx.sum(), len(bad_idx), y.min(), y.max(), x.min(), x.max()))
    return y[total_wing:-total_wing]
