import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.filteringSegm import squash_by_groups, require_column


@require_column('sem')
def sem(segarr, zscore=1.96):
    margin = segarr['sem'] * zscore
    levels = np.zeros(len(segarr))
    levels[segarr['log2'] - margin > 0] = 1
    levels[segarr['log2'] + margin < 0] = -1
    return squash_by_groups(segarr, pd.Series(levels))
