from pynguin.dataset.cnvkit.call import get_as_dframe_and_set_reference_and_expect_copies


def absolute_expect(cnarr, ploidy, diploid_parx_genome, is_sample_female):
    """Absolute integer number of expected copies in each bin.

    I.e. the given ploidy for autosomes, and XY or XX sex chromosome counts
    according to the sample's specified chromosomal sex.
    """
    is_haploid_x_reference = True
    df = get_as_dframe_and_set_reference_and_expect_copies(cnarr, ploidy, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
    exp_copies = df['expect']
    return exp_copies
