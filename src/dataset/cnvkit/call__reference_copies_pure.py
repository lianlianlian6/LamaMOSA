def _reference_copies_pure(chrom, ploidy, is_haploid_x_reference):
    """Determine the reference number of chromosome copies (pure sample).

    Returns
    -------
    int
        Number of copies in the reference.
    """
    chrom = chrom.lower()
    if chrom in ['chry', 'y'] or (is_haploid_x_reference and chrom in ['chrx', 'x']):
        ref_copies = ploidy // 2
    else:
        ref_copies = ploidy
    return ref_copies
