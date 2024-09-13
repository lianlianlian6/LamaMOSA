import numpy as np

from pynguin.dataset.cnvkit.call import _reference_copies_pure, _log2_ratio_to_absolute_pure


def absolute_pure(cnarr, ploidy, is_haploid_x_reference):
    """Calculate absolute copy number values from segment or bin log2 ratios."""
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    for (i, row) in enumerate(cnarr):
        ref_copies = _reference_copies_pure(row.chromosome, ploidy, is_haploid_x_reference)
        absolutes[i] = _log2_ratio_to_absolute_pure(row.log2, ref_copies)
    return absolutes
