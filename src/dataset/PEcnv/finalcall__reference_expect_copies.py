def _reference_expect_copies(chrom, ploidy, is_sample_female, is_reference_male):
    chrom = chrom.lower()
    if chrom in ['chrx', 'x']:
        ref_copies = ploidy // 2 if is_reference_male else ploidy
        exp_copies = ploidy if is_sample_female else ploidy // 2
    elif chrom in ['chry', 'y']:
        ref_copies = ploidy // 2
        exp_copies = 0 if is_sample_female else ploidy // 2
    else:
        ref_copies = exp_copies = ploidy
    return (ref_copies, exp_copies)
