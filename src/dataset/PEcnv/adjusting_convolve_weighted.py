import logging
import numpy as np

def convolve_weighted(window, signal, weights, n_iter=1):
    assert len(weights) == len(signal), 'len(weights) = %d, len(signal) = %d, window_size = %s' % (len(weights), len(signal), len(window))
    (y, w) = (signal, weights)
    window /= window.sum()
    for _i in range(n_iter):
        logging.debug('Iteration %d: len(y)=%d, len(w)=%d', _i, len(y), len(w))
        D = np.convolve(w * y, window, mode='same')
        N = np.convolve(w, window, mode='same')
        y = D / N
        w = np.convolve(window, w, mode='same')
    return (y, w)
