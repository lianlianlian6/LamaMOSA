import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.finalcall import _reference_expect_copies, _log2_ratio_to_absolute


def absolute_dataframe(cnarr, ploidy, purity, is_reference_male, is_sample_female):
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    reference_copies = expect_copies = np.zeros(len(cnarr), dtype=np.int_)
    for (i, row) in enumerate(cnarr):
        (ref_copies, exp_copies) = _reference_expect_copies(row.chromosome, ploidy, is_sample_female, is_reference_male)
        reference_copies[i] = ref_copies
        expect_copies[i] = exp_copies
        absolutes[i] = _log2_ratio_to_absolute(row.log2, ref_copies, exp_copies, purity)
    return pd.DataFrame({'absolute': absolutes, 'reference': reference_copies, 'expect': expect_copies})
