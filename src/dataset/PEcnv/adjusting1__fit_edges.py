from pynguin.dataset.PEcnv.adjusting import _fit_edge


def _fit_edges(x, y, wing, polyorder=3):
    window_length = 2 * wing + 1
    n = len(x)
    _fit_edge(x, y, 0, window_length, 0, wing, polyorder)
    _fit_edge(x, y, n - window_length, n, n - wing, n, polyorder)
