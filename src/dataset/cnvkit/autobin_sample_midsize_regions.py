import numpy as np

def sample_midsize_regions(regions, max_num):
    """Randomly select a subset of up to `max_num` regions."""
    sizes = regions.end - regions.start
    (lo_size, hi_size) = np.percentile(sizes[sizes > 0], [25, 75])
    midsize_regions = regions.data[(sizes >= lo_size) & (sizes <= hi_size)]
    if len(midsize_regions) > max_num:
        midsize_regions = midsize_regions.sample(max_num, random_state=679661)
    return midsize_regions
