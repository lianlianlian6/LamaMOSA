
import numpy as np

from pynguin.dataset.PEcnv.adjusting import check_inputs


def rolling_std(x, width):
    (x, wing, signal) = check_inputs(x, width)
    rolled = signal.rolling(2 * wing + 1, 2, center=True).std()
    return np.asfarray(rolled[wing:-wing])
