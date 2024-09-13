import numpy as np

from pynguin.dataset.PEcnv.plots import get_repeat_slices


def update_binwise_positions(cnarr, segments=None, variants=None):
    cnarr = cnarr.copy()
    if segments:
        segments = segments.copy()
        seg_chroms = set(segments.chromosome.unique())
    if variants:
        variants = variants.copy()
        var_chroms = set(variants.chromosome.unique())
    for chrom in cnarr.chromosome.unique():
        c_idx = cnarr.chromosome == chrom
        c_bins = cnarr[c_idx]
        if segments and chrom in seg_chroms:
            c_seg_idx = (segments.chromosome == chrom).values
            seg_starts = np.searchsorted(c_bins.start.values, segments.start.values[c_seg_idx])
            seg_ends = np.r_[seg_starts[1:], len(c_bins)]
            segments.data.loc[c_seg_idx, 'start'] = seg_starts
            segments.data.loc[c_seg_idx, 'end'] = seg_ends
        if variants and chrom in var_chroms:
            c_varr_idx = (variants.chromosome == chrom).values
            c_varr_df = variants.data[c_varr_idx]
            v_starts = np.searchsorted(c_bins.start.values, c_varr_df.start.values)
            for (idx, size) in list(get_repeat_slices(v_starts)):
                v_starts[idx] += np.arange(size) / size
            variant_sizes = c_varr_df.end - c_varr_df.start
            variants.data.loc[c_varr_idx, 'start'] = v_starts
            variants.data.loc[c_varr_idx, 'end'] = v_starts + variant_sizes
        c_starts = np.arange(len(c_bins))
        c_ends = np.arange(1, len(c_bins) + 1)
        cnarr.data.loc[c_idx, 'start'] = c_starts
        cnarr.data.loc[c_idx, 'end'] = c_ends
    return (cnarr, segments, variants)
