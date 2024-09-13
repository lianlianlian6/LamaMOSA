import numpy as np
from scipy import stats
from pynguin.dataset.PEcnv import measures
from pynguin.dataset.PEcnv.segmIndicators import calc_intervals


def do_segmetrics(cnarr, segarr, location_stats=(), spread_stats=(), interval_stats=(), alpha=0.05, bootstraps=100, smoothed=False):
    import warnings
    warnings.simplefilter('ignore', RuntimeWarning)
    stat_funcs = {'mean': np.mean, 'median': np.median, 'mode': measures.modal_location, 'p_ttest': lambda a: stats.ttest_1samp(a, 0.0, nan_policy='omit')[1], 'stdev': np.std, 'mad': measures.median_absolute_deviation, 'mse': measures.mean_squared_error, 'iqr': measures.interquartile_range, 'bivar': measures.biweight_midvariance, 'sem': stats.sem, 'ci': make_ci_func(alpha, bootstraps, smoothed), 'pi': make_pi_func(alpha)}
    bins_log2s = list(cnarr.iter_ranges_of(segarr, 'log2', 'outer', True))
    segarr = segarr.copy()
    if location_stats:
        for statname in location_stats:
            func = stat_funcs[statname]
            segarr[statname] = np.fromiter(map(func, bins_log2s), np.float_, len(segarr))
    if spread_stats:
        deviations = (bl - sl for (bl, sl) in zip(bins_log2s, segarr['log2']))
        if len(spread_stats) > 1:
            deviations = list(deviations)
        for statname in spread_stats:
            func = stat_funcs[statname]
            segarr[statname] = np.fromiter(map(func, deviations), np.float_, len(segarr))
    weights = cnarr['weight']
    if 'ci' in interval_stats:
        (segarr['ci_lo'], segarr['ci_hi']) = calc_intervals(bins_log2s, weights, stat_funcs['ci'])
    if 'pi' in interval_stats:
        (segarr['pi_lo'], segarr['pi_hi']) = calc_intervals(bins_log2s, weights, stat_funcs['pi'])
    return segarr
