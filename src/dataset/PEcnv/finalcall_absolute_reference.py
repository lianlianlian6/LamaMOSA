import numpy as np

def absolute_reference(cnarr, ploidy, is_reference_male):
    ref_copies = np.repeat(ploidy, len(cnarr))
    is_x = (cnarr.chromosome == cnarr._chr_x_label).values
    is_y = (cnarr.chromosome == cnarr._chr_y_label).values
    if is_reference_male:
        ref_copies[is_x] = ploidy // 2
    ref_copies[is_y] = ploidy // 2
    return ref_copies
