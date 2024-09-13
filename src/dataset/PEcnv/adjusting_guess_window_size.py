from pynguin.dataset.PEcnv import measures


def guess_window_size(x, weights=None):
    if weights is None:
        sd = measures.biweight_midvariance(x)
    else:
        sd = measures.weighted_std(x, weights)
    width = 4 * sd * len(x) ** (4 / 5)
    width = max(3, int(round(width)))
    width = min(len(x), width)
    return width
