import pandas as pd
from pynguin.dataset.PEcnv import filteringSegm

def spike_into_segments(cnarr, segments, is_sig):
    if is_sig.any():
        cnarr['is_sig'] = is_sig
        chunks = []
        for (segment, seghits) in cnarr.by_ranges(segments, keep_empty=True):
            if seghits['is_sig'].any():
                levels = seghits['is_sig'].cumsum() * seghits['is_sig']
                chunks.append(seghits.data.assign(_levels=levels).groupby('_levels', sort=False).apply(filteringSegm.squash_region).reset_index(drop=True))
            else:
                chunks.append(pd.DataFrame.from_records([segment], columns=segments.data.columns))
        return cnarr.as_dataframe(pd.concat(chunks))
    else:
        return segments
