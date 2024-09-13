import numpy as np

def log2_ratios(cnarr, absolutes, ploidy, is_reference_male, min_abs_val=0.001, round_to_int=False):
    if round_to_int:
        absolutes = absolutes.round()
    ratios = np.log2(np.maximum(absolutes / ploidy, min_abs_val))
    if is_reference_male:
        ratios[(cnarr.chromosome == cnarr._chr_x_label).values] += 1.0
    ratios[(cnarr.chromosome == cnarr._chr_y_label).values] += 1.0
    return ratios
