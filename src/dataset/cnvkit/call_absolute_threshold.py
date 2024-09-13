import logging
import numpy as np

from pynguin.dataset.cnvkit.call import _reference_copies_pure, _log2_ratio_to_absolute_pure


def absolute_threshold(cnarr, ploidy, thresholds, is_haploid_x_reference):
    """Call integer copy number using hard thresholds for each level.

    Integer values are assigned for log2 ratio values less than each given
    threshold value in sequence, counting up from zero.
    Above the last threshold value, integer copy numbers are called assuming
    full purity, diploidy, and rounding up.

    Default thresholds follow this heuristic for calling CNAs in a tumor sample:
    For single-copy gains and losses, assume 50% tumor cell clonality (including
    normal cell contamination). Then::

        R> log2(2:6 / 4)
        -1.0  -0.4150375  0.0  0.3219281  0.5849625

    Allowing for random noise of +/- 0.1, the cutoffs are::

        DEL(0)  <  -1.1
        LOSS(1) <  -0.25
        GAIN(3) >=  +0.2
        AMP(4)  >=  +0.7

    For germline samples, better precision could be achieved with::

        LOSS(1) <  -0.4
        GAIN(3) >=  +0.3

    """
    absolutes = np.zeros(len(cnarr), dtype=np.float_)
    for (idx, row) in enumerate(cnarr):
        ref_copies = _reference_copies_pure(row.chromosome, ploidy, is_haploid_x_reference)
        if np.isnan(row.log2):
            logging.warning('log2=nan found; replacing with neutral copy number %s', ref_copies)
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
