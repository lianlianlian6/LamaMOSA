from pynguin.dataset.cnvkit.access import drop_noncanonical_contigs
from pynguin.dataset.cnvkit.antitarget import guess_chromosome_regions
from pynguin.dataset.cnvkit.params import INSERT_SIZE, MIN_REF_COVERAGE, ANTITARGET_NAME

def get_antitargets(targets, accessible, avg_bin_size, min_bin_size):
    """Generate antitarget intervals between/around target intervals.

    Procedure:

    - Invert target intervals
    - Subtract the inverted targets from accessible regions
    - For each of the resulting regions:

        - Shrink by a fixed margin on each end
        - If it's smaller than min_bin_size, skip
        - Divide into equal-size (region_size/avg_bin_size) portions
        - Emit the (chrom, start, end) coords of each portion
    """
    if accessible:
        accessible = drop_noncanonical_contigs(accessible, targets)
    else:
        TELOMERE_SIZE = 150000
        accessible = guess_chromosome_regions(targets, TELOMERE_SIZE)
    pad_size = 2 * INSERT_SIZE
    bg_arr = accessible.resize_ranges(-pad_size).subtract(targets.resize_ranges(pad_size)).subdivide(avg_bin_size, min_bin_size)
    bg_arr['gene'] = ANTITARGET_NAME
    return bg_arr
