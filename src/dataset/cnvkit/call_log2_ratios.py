import numpy as np

def log2_ratios(cnarr, absolutes, ploidy, is_haploid_x_reference, diploid_parx_genome, min_abs_val=0.001, round_to_int=False):
    """Convert absolute copy numbers to log2 ratios.

    Optionally round copy numbers to integers.

    Account for reference sex & ploidy of sex chromosomes.
    """
    if round_to_int:
        absolutes = absolutes.round()
    ratios = np.log2(np.maximum(absolutes / ploidy, min_abs_val))
    if is_haploid_x_reference:
        ratios[cnarr.chr_x_filter(diploid_parx_genome).values] += 1.0
    ratios[cnarr.chr_y_filter(diploid_parx_genome).values] += 1.0
    return ratios
