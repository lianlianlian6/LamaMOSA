import logging
import numpy as np
from scipy import stats

def _bca_correct_alpha(values, weights, bootstrap_dist, alphas):
    n_boots = len(bootstrap_dist)
    orig_mean = np.average(values, weights=weights)
    n_boots_below = (bootstrap_dist < orig_mean).sum()
    if n_boots_below == 0:
        logging.warning('boots mean %s, orig mean %s', bootstrap_dist.mean(), orig_mean)
    else:
        logging.warning('boot samples less: %s / %s', n_boots_below, n_boots)
    z0 = stats.norm.ppf((bootstrap_dist < orig_mean).sum() / n_boots)
    zalpha = stats.norm.ppf(alphas)
    u = np.array([np.average(np.concatenate([values[:i], values[i + 1:]]), weights=np.concatenate([weights[:i], weights[i + 1:]])) for i in range(len(values))])
    uu = u.mean() - u
    acc = (u ** 3).sum() / (6 * (uu ** 2).sum() ** 1.5)
    alphas = stats.norm.cdf(z0 + (z0 + zalpha) / (1 - acc * (z0 + zalpha)))
    if not 0 < alphas[0] < 1 and 0 < alphas[1] < 1:
        raise ValueError('CI alphas should be in (0,1); got %s' % alphas)
    return alphas
