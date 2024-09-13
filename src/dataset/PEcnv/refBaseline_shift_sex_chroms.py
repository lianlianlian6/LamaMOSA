def shift_sex_chroms(cnarr, sexes, ref_flat_logr, is_chr_x, is_chr_y):
    is_xx = sexes.get(cnarr.sample_id)
    cnarr['log2'] += ref_flat_logr
    if is_xx:
        cnarr[is_chr_y, 'log2'] = -1.0
    else:
        cnarr[is_chr_x | is_chr_y, 'log2'] += 1.0
