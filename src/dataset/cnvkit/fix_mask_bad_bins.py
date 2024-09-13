
from pynguin.dataset.cnvkit import params

def mask_bad_bins(cnarr):
    """Flag the bins with excessively low or inconsistent coverage.

    Returns
    -------
    np.array
        A boolean array where True indicates bins that failed the checks.
    """
    mask = (cnarr['log2'] < params.MIN_REF_COVERAGE) | (cnarr['log2'] > -params.MIN_REF_COVERAGE) | (cnarr['spread'] > params.MAX_REF_SPREAD)
    if 'depth' in cnarr:
        mask |= cnarr['depth'] == 0
    if 'gc' in cnarr:
        assert params.GC_MIN_FRACTION >= 0 and params.GC_MIN_FRACTION <= 1
        assert params.GC_MAX_FRACTION >= 0 and params.GC_MAX_FRACTION <= 1
        lower_gc_bound = min(params.GC_MIN_FRACTION, params.GC_MAX_FRACTION)
        upper_gc_bound = max(params.GC_MIN_FRACTION, params.GC_MAX_FRACTION)
        mask |= (cnarr['gc'] > upper_gc_bound) | (cnarr['gc'] < lower_gc_bound)
    return mask
