import numpy as np

def get_as_dframe_and_set_reference_and_expect_copies(cnarr, ploidy, is_haploid_x_reference, diploid_parx_genome, is_sample_female):
    """Determine the number copies of a chromosome expected and in reference.

    For sex chromosomes, these values may not be the same ploidy as the
    autosomes. The "reference" number is the chromosome's ploidy in the
    CNVkit reference, while "expect" is the chromosome's neutral ploidy in the
    given sample, based on the specified sex of each. E.g., given a female
    sample and a male reference, on chromosome X the "reference" value is 1 but
    "expect" is 2. Note that the "reference" value for chromosome Y is always 1
    (better: `ploidy / 2`, see implementation below) to avoid divide-by-zero
    problems. The default reference is thus XXY (i.e. Klinefelter syndrome).

    Returns
    -------
    tuple
        A pair of integers: number of copies in the reference, and expected in
        the sample.
    """
    df = cnarr.copy().data
    df['reference'] = np.repeat(ploidy, len(df))
    df['expect'] = np.repeat(ploidy, len(df))
    df.loc[cnarr.chr_x_filter(diploid_parx_genome), 'reference'] = ploidy // 2 if is_haploid_x_reference else ploidy
    df.loc[cnarr.chr_x_filter(diploid_parx_genome), 'expect'] = ploidy if is_sample_female else ploidy // 2
    df.loc[cnarr.chr_y_filter(diploid_parx_genome), 'reference'] = ploidy // 2
    df.loc[cnarr.chr_y_filter(diploid_parx_genome), 'expect'] = 0 if is_sample_female else ploidy // 2
    if diploid_parx_genome is not None:
        df.loc[cnarr.pary_filter(diploid_parx_genome), 'reference'] = 0
        df.loc[cnarr.pary_filter(diploid_parx_genome), 'expect'] = 0
    return df
