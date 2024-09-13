
import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.filteringSegm import require_column, squash_by_groups


@require_column('cn')
def ampdel(segarr):
    levels = np.zeros(len(segarr))
    levels[segarr['cn'] == 0] = -1
    levels[segarr['cn'] >= 5] = 1
    cnarr = squash_by_groups(segarr, pd.Series(levels))
    return cnarr[(cnarr['cn'] == 0) | (cnarr['cn'] >= 5)]
