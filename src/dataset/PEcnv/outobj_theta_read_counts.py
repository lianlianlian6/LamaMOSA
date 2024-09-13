def theta_read_counts(log2_ratio, nbins, avg_depth=500, avg_bin_width=200, read_len=100):
    read_depth = 2 ** log2_ratio * avg_depth
    read_count = nbins * avg_bin_width * read_depth / read_len
    return read_count.round().fillna(0).astype('int')
