import numpy as np
import pandas as pd

def _allele_specific_copy_numbers(segarr, varr, ploidy=2):
    """Split total copy number between alleles based on BAF.

    See: PSCBS, Bentsson et al. 2011
    """
    seg_depths = ploidy * np.exp2(segarr['log2'])
    seg_bafs = varr.baf_by_ranges(segarr, above_half=True)
    cn1 = 0.5 * (1 - seg_bafs) * seg_depths
    cn2 = seg_depths - cn1
    return pd.DataFrame({'baf': seg_bafs, 'cn1': cn1, 'cn2': cn2})
