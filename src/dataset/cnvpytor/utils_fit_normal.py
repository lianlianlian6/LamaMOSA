from __future__ import absolute_import, print_function, division
import numpy as np
from scipy.optimize import curve_fit
import logging

from pynguin.dataset.cnvpytor import normal

_logger = logging.getLogger("cnvpytor.utils")
def fit_normal(x, y):
    """ Fit Gaussian
    """
    if sum(y) == 0:
        _logger.debug('Problem with fit: all data points have zero value. Return zeros instead fit parameters!')
        return ([0, 0, 0], None)
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))
    area = sum(y[:-1] * (x[1:] - x[:-1]))
    _logger.debug('%f %f %f %d' % (area, mean, sigma, len(x)))
    if sigma == 0:
        _logger.debug('Problem with fit: sigma equals zero. Using mean and std instead fitting parameters!')
        return ([area, mean, sigma], None)
    if len(x) < 3:
        _logger.warning('Problem with fit: insufficient data points. Using mean and std instead fitting parameters!')
        return ([area, mean, sigma], None)
    try:
        (popt, pcov) = curve_fit(normal, x, y, p0=[area, mean, sigma])
        popt[2] = np.abs(popt[2])
        if popt[1] <= 0:
            _logger.warning('Problem with fit: negative mean. Using mean and std instead fitting parameters!')
            return ([area, mean, sigma], None)
        return (popt, pcov)
    except ValueError:
        _logger.warning('Problem with fit: Value Error. Using mean and std instead fitting parameters!')
        return ([area, mean, sigma], None)
    except RuntimeError:
        _logger.warning('Problem with fit: Runtime Error. Using mean and std instead fitting parameters!')
        return ([area, mean, sigma], None)
