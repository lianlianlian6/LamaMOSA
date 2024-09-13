import numpy as np

from pynguin.dataset.PEcnv.finalcall import _reference_expect_copies, _log2_ratio_to_absolute


def absolute_clonal(cnarr, ploidy, purity, is_reference_male, is_sample_female):
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    for (i, row) in enumerate(cnarr):
        (ref_copies, expect_copies) = _reference_expect_copies(row.chromosome, ploidy, is_sample_female, is_reference_male)
        absolutes[i] = _log2_ratio_to_absolute(row.log2, ref_copies, expect_copies, purity)
    return absolutes
