import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.filteringSegm import require_column, squash_by_groups


@require_column('ci_lo', 'ci_hi')
def ci(segarr):
    levels = np.zeros(len(segarr))
    levels[segarr['ci_lo'].values > 0] = 1
    levels[segarr['ci_hi'].values < 0] = -1
    return squash_by_groups(segarr, pd.Series(levels))
