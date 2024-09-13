def _log2_ratio_to_absolute_pure(log2_ratio, ref_copies):
    """Transform a log2 ratio to absolute linear scale (for a pure sample).

    Purity adjustment is skipped. This is appropriate if the sample is germline
    or if scaling for tumor heterogeneity was done beforehand.

    .. math :: n = r*2^v
    """
    ncopies = ref_copies * 2 ** log2_ratio
    return ncopies
