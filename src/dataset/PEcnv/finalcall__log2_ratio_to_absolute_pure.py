def _log2_ratio_to_absolute_pure(log2_ratio, ref_copies):
    ncopies = ref_copies * 2 ** log2_ratio
    return ncopies
