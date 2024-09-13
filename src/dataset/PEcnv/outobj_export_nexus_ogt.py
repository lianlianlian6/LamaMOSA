def export_nexus_ogt(cnarr, varr, min_weight=0.0):
    if min_weight and 'weight' in cnarr:
        mask_low_weight = cnarr['weight'] < min_weight
        cnarr.data = cnarr.data[~mask_low_weight]
    bafs = varr.baf_by_ranges(cnarr)
    out_table = cnarr.data.reindex(columns=['chromosome', 'start', 'end', 'log2'])
    out_table = out_table.rename(columns={'chromosome': 'Chromosome', 'start': 'Position', 'end': 'Position', 'log2': 'Log R Ratio'})
    out_table['B-Allele Frequency'] = bafs
    return out_table
