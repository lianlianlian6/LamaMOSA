
import numpy as np

from pynguin.dataset.PEcnv.segmIndicators import _smooth_samples_by_weight


def confidence_interval_bootstrap(values, weights, alpha, bootstraps=100, smoothed=False):
    if not 0 < alpha < 1:
        raise ValueError('alpha must be between 0 and 1; got %s' % alpha)
    if bootstraps <= 2 / alpha:
        new_boots = int(np.ceil(2 / alpha))
        bootstraps = new_boots
    k = len(values)
    if k < 2:
        return np.repeat(values[0], 2)
    np.random.seed(679661)
    rand_indices = np.random.randint(0, k, size=(bootstraps, k))
    samples = ((np.take(values, idx), np.take(weights, idx)) for idx in rand_indices)
    if smoothed:
        samples = _smooth_samples_by_weight(values, samples)
    seg_means = (np.average(val, weights=wt) for (val, wt) in samples)
    bootstrap_dist = np.fromiter(seg_means, np.float_, bootstraps)
    alphas = np.array([alpha / 2, 1 - alpha / 2])
    if not smoothed:
        pass
    ci = np.percentile(bootstrap_dist, list(100 * alphas))
    return ci
