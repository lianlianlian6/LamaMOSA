import pandas as pd

def do_metrics(cnarrs, segments=None, skip_low=False):
    from .cnv import CopyNumArray as CNA
    if isinstance(cnarrs, CNA):
        cnarrs = [cnarrs]
    if isinstance(segments, CNA):
        segments = [segments]
    elif segments is None:
        segments = [None]
    else:
        segments = list(segments)
    if skip_low:
        cnarrs = (cna.drop_low_coverage() for cna in cnarrs)
    rows = ((cna.meta.get('filename', cna.sample_id), len(seg) if seg is not None else '-') + ests_of_scale(cna.residuals(seg).values) for (cna, seg) in zip_repeater(cnarrs, segments))
    colnames = ['sample', 'segments', 'stdev', 'mad', 'iqr', 'bivar']
    return pd.DataFrame.from_records(rows, columns=colnames)
