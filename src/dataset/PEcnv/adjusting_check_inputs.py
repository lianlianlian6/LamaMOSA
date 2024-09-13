import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.adjusting import _width2wing, _pad_array


def check_inputs(x, width, as_series=True, weights=None):
    x = np.asfarray(x)
    wing = _width2wing(width, x)
    signal = _pad_array(x, wing)
    if as_series:
        signal = pd.Series(signal)
    if weights is None:
        return (x, wing, signal)
    weights = _pad_array(weights, wing)
    weights[:wing] *= np.linspace(1 / wing, 1, wing)
    weights[-wing:] *= np.linspace(1, 1 / wing, wing)
    if as_series:
        weights = pd.Series(weights)
    return (x, wing, signal, weights)
