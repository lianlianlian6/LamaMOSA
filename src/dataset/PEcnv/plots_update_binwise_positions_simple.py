import numpy as np

def update_binwise_positions_simple(cnarr):
    start_chunks = []
    end_chunks = []
    is_segment = 'probes' in cnarr
    if is_segment:
        cnarr = cnarr[cnarr['probes'] > 0]
    for (_chrom, c_arr) in cnarr.by_chromosome():
        if is_segment:
            ends = c_arr['probes'].values.cumsum()
            starts = np.r_[0, ends[:-1]]
        else:
            n_bins = len(c_arr)
            starts = np.arange(n_bins)
            ends = np.arange(1, n_bins + 1)
        start_chunks.append(starts)
        end_chunks.append(ends)
    return cnarr.as_dataframe(cnarr.data.assign(start=np.concatenate(start_chunks), end=np.concatenate(end_chunks)))
