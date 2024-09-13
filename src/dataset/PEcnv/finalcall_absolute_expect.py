import numpy as np

def absolute_expect(cnarr, ploidy, is_sample_female):
    exp_copies = np.repeat(ploidy, len(cnarr))
    is_y = (cnarr.chromosome == cnarr._chr_y_label).values
    if is_sample_female:
        exp_copies[is_y] = 0
    else:
        is_x = (cnarr.chromosome == cnarr._chr_x_label).values
        exp_copies[is_x | is_y] = ploidy // 2
    return exp_copies
