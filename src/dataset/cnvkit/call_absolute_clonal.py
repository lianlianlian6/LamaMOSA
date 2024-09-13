from pynguin.dataset.cnvkit.call import absolute_dataframe


def absolute_clonal(cnarr, ploidy, purity, is_haploid_x_reference, diploid_parx_genome, is_sample_female):
    """Calculate absolute copy number values from segment or bin log2 ratios."""
    df = absolute_dataframe(cnarr, ploidy, purity, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
    return df['absolute']
