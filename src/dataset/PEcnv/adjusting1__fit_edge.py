import numpy as np

def _fit_edge(x, y, window_start, window_stop, interp_start, interp_stop, polyorder):
    x_edge = x[window_start:window_stop]
    poly_coeffs = np.polyfit(np.arange(0, window_stop - window_start), x_edge, polyorder)
    i = np.arange(interp_start - window_start, interp_stop - window_start)
    values = np.polyval(poly_coeffs, i)
    y[interp_start:interp_stop] = values
