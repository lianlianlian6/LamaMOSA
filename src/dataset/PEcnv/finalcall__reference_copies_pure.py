
def _reference_copies_pure(chrom, ploidy, is_reference_male):
    chrom = chrom.lower()
    if chrom in ['chry', 'y'] or (is_reference_male and chrom in ['chrx', 'x']):
        ref_copies = ploidy // 2
    else:
        ref_copies = ploidy
    return ref_copies
