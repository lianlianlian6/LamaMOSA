import numpy as np

def convolve_unweighted(window, signal, wing, n_iter=1):
    window /= window.sum()
    y = signal
    for _i in range(n_iter):
        y = np.convolve(window, y, mode='same')
    y = y[wing:-wing]
    return y
