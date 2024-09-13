import numpy as np

def segment_mean(cnarr, skip_low=False):
    """Weighted average of bin log2 values."""
    if skip_low:
        cnarr = cnarr.drop_low_coverage()
    if len(cnarr) == 0:
        return np.nan
    if 'weight' in cnarr and cnarr['weight'].any():
        return np.average(cnarr['log2'], weights=cnarr['weight'])
    return cnarr['log2'].mean()
