from __future__ import absolute_import, print_function, division
import numpy as np
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import OptimizeWarning
import logging

from pynguin.dataset.cnvpytor import bimodal

_logger = logging.getLogger("cnvpytor.utils")
def fit_bimodal(x, y):
    """ Fit double Gaussian
    """
    if sum(y) == 0:
        _logger.debug('Problem with fit: all data points have zero value. Return None!')
        return None
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    area = sum(y[:-1] * (x[1:] - x[:-1]))
    _logger.debug('%f %f %f %d' % (area, mean, sigma, len(x)))
    if sigma == 0:
        _logger.debug('Problem with fit: sigma equals zero. Return None!')
        return None
    if len(x) < 3:
        _logger.warning('Problem with fit: insufficient data points. Return None!')
        return None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', OptimizeWarning)
            (popt, pcov) = curve_fit(bimodal, x, y, p0=[area / 2, mean * 0.66, sigma / 2, area / 2, mean * 1.33, sigma / 2])
            return (popt, pcov)
    except OptimizeWarning:
        _logger.warning('Problem with fit: OptimizeWarning. Return None!')
        return None
    except ValueError:
        _logger.warning('Problem with fit: Value Error. Return None!')
        return None
    except RuntimeError:
        _logger.warning('Problem with fit: Runtime Error. Return None!')
        return None
