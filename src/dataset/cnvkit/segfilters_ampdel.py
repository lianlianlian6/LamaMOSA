
import numpy as np
import pandas as pd

from pynguin.dataset.cnvkit.segfilters import squash_by_groups


def ampdel(segarr):
    """Merge segments by amplified/deleted/neutral copy number status.

    Follow the clinical reporting convention:

    - 5+ copies (2.5-fold gain) is amplification
    - 0 copies is homozygous/deep deletion
    - CNAs of lesser degree are not reported

    This is recommended only for selecting segments corresponding to
    actionable, usually focal, CNAs. Any real and potentially informative but
    lower-level CNAs will be dropped.
    """
    levels = np.zeros(len(segarr))
    levels[segarr['cn'] == 0] = -1
    levels[segarr['cn'] >= 5] = 1
    cnarr = squash_by_groups(segarr, pd.Series(levels))
    return cnarr[(cnarr['cn'] == 0) | (cnarr['cn'] >= 5)]
