from pynguin.dataset.cnvkit.call import get_as_dframe_and_set_reference_and_expect_copies


def absolute_reference(cnarr, ploidy, diploid_parx_genome, is_haploid_x_reference):
    """Absolute integer number of reference copies in each bin.

    I.e. the given ploidy for autosomes, 1 or 2 X according to the reference
    sex, and always 1 copy of Y.
    """
    is_sample_female = True
    df = get_as_dframe_and_set_reference_and_expect_copies(cnarr, ploidy, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
    ref_copies = df['reference']
    return ref_copies
