import logging
import numpy as np
from pynguin.dataset.cnvkit.plots import MB
def set_xlim_from(axis, probes=None, segments=None, variants=None):
    """Configure axes for plotting a single chromosome's data.

    Parameters
    ----------
    probes : CopyNumArray
    segments : CopyNumArray
    variants : VariantArray
        All should already be subsetted to the region that will be plotted.
    """
    min_x = np.inf
    max_x = 0
    for arr in (probes, segments, variants):
        if arr and len(arr):
            max_x = max(max_x, arr.end.iat[-1])
            min_x = min(min_x, arr.start.iat[0])
    if max_x <= min_x:
        if min_x != np.inf:
            logging.warning('WARNING: selection start %s > end %s; did you correctly sort the input file by genomic location?', min_x, max_x)
        raise ValueError(f'No usable data points to plot out of {(len(probes) if probes else 0)} probes, {(len(segments) if segments else 0)} segments, {(len(variants) if variants else 0)} variants')
    axis.set_xlim(min_x * MB, max_x * MB)
