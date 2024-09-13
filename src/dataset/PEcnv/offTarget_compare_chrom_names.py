def compare_chrom_names(a_regions, b_regions):
    a_chroms = set(a_regions.chromosome.unique())
    b_chroms = set(b_regions.chromosome.unique())
    if a_chroms and a_chroms.isdisjoint(b_chroms):
        msg = 'Chromosome names do not match between files'
        a_fname = a_regions.meta.get('filename')
        b_fname = b_regions.meta.get('filename')
        if a_fname and b_fname:
            msg += ' {} and {}'.format(a_fname, b_fname)
        msg += ': {} vs. {}'.format(', '.join(map(repr, sorted(a_chroms)[:3])), ', '.join(map(repr, sorted(b_chroms)[:3])))
        raise ValueError(msg)
    return (a_chroms, b_chroms)
