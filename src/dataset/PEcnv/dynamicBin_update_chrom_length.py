from pynguin.dataset.PEcnv.dynamicBin import region_size_by_chrom


def update_chrom_length(rc_table, regions):
    if regions is not None and len(regions):
        chrom_sizes = region_size_by_chrom(regions)
        rc_table = rc_table.merge(chrom_sizes, on='chromosome', how='inner')
        rc_table['length'] = rc_table['length_y']
        rc_table = rc_table.drop(['length_x', 'length_y'], axis=1)
    return rc_table
