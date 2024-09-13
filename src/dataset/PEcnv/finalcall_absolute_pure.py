import numpy as np

from pynguin.dataset.PEcnv.finalcall import _reference_copies_pure, _log2_ratio_to_absolute_pure


def absolute_pure(cnarr, ploidy, is_reference_male):
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    for (i, row) in enumerate(cnarr):
        ref_copies = _reference_copies_pure(row.chromosome, ploidy, is_reference_male)
        absolutes[i] = _log2_ratio_to_absolute_pure(row.log2, ref_copies)
    return absolutes
