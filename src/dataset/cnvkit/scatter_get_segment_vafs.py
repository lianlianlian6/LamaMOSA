import numpy as np

def get_segment_vafs(variants, segments):
    """Group SNP allele frequencies by segment.

    Assume variants and segments were already subset to one chromosome.

    Yields
    ------
    tuple
        (segment, value)
    """
    if segments:
        chunks = variants.by_ranges(segments)
    else:
        chunks = [(None, variants)]
    for (seg, seg_snvs) in chunks:
        freqs = seg_snvs['alt_freq'].values
        idx_above_mid = freqs > 0.5
        for idx_vaf in (idx_above_mid, ~idx_above_mid):
            if sum(idx_vaf) > 1:
                yield (seg, np.median(freqs[idx_vaf]))
