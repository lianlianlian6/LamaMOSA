import numpy as np

from pynguin.dataset.PEcnv.finalcall import _reference_copies_pure, _log2_ratio_to_absolute_pure


def absolute_threshold(cnarr, ploidy, thresholds, is_reference_male):
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    for (idx, row) in enumerate(cnarr):
        ref_copies = _reference_copies_pure(row.chromosome, ploidy, is_reference_male)
        if np.isnan(row.log2):
            absolutes[idx] = ref_copies
            continue
        cnum = 0
        for (cnum, thresh) in enumerate(thresholds):
            if row.log2 <= thresh:
                if ref_copies != ploidy:
                    cnum = int(cnum * ref_copies / ploidy)
                break
        else:
            cnum = int(np.ceil(_log2_ratio_to_absolute_pure(row.log2, ref_copies)))
        absolutes[idx] = cnum
    return absolutes
