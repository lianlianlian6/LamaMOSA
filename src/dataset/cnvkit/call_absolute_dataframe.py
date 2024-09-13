from pynguin.dataset.cnvkit.call import get_as_dframe_and_set_reference_and_expect_copies, _log2_ratio_to_absolute


def absolute_dataframe(cnarr, ploidy, purity, is_haploid_x_reference, diploid_parx_genome, is_sample_female):
    """Absolute, expected and reference copy number in a DataFrame."""
    df = get_as_dframe_and_set_reference_and_expect_copies(cnarr, ploidy, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
    df['absolute'] = df.apply(lambda row: _log2_ratio_to_absolute(row['log2'], row['reference'], row['expect'], purity), axis=1)
    return df[['absolute', 'expect', 'reference']]
