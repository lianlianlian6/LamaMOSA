def theta_read_counts(log2_ratio, nbins, avg_depth=500, avg_bin_width=200, read_len=100):
    """Calculate segments' read counts from log2-ratios.

    Math:
        nbases = read_length * read_count
    and
        nbases = bin_width * read_depth
    where
        read_depth = read_depth_ratio * avg_depth

    So:
        read_length * read_count = bin_width * read_depth
        read_count = bin_width * read_depth / read_length
    """
    read_depth = 2 ** log2_ratio * avg_depth
    read_count = nbins * avg_bin_width * read_depth / read_len
    return read_count.round().fillna(0).astype('int')
