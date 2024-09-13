from pynguin.dataset.PEcnv.finalcall import _log2_ratio_to_absolute_pure


def _log2_ratio_to_absolute(log2_ratio, ref_copies, expect_copies, purity=None):
    if purity and purity < 1.0:
        ncopies = (ref_copies * 2 ** log2_ratio - expect_copies * (1 - purity)) / purity
    else:
        ncopies = _log2_ratio_to_absolute_pure(log2_ratio, ref_copies)
    return ncopies
