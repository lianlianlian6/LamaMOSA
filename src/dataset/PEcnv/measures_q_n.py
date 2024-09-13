import numpy as np

from pynguin.dataset.PEcnv.measures import on_array


@on_array(0)
def q_n(a):
    vals = []
    for (i, x_i) in enumerate(a):
        for x_j in a[i + 1:]:
            vals.append(abs(x_i - x_j))
    quartile = np.percentile(vals, 25)
    n = len(a)
    if n <= 10:
        scale = 1.392
    elif 10 < n < 400:
        scale = 1.0 + 4 / n
    else:
        scale = 1.0
    return quartile / scale
