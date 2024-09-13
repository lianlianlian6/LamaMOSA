import numpy as np
from pynguin.dataset.PEcnv import hyperparameters
from pynguin.dataset.PEcnv.segmIndicators import segment_mean

def group_by_genes(cnarr, skip_low):
    ignore = ('', np.nan) + hyperparameters.OFFTARGET_ALIASES
    for (gene, rows) in cnarr.by_gene():
        if not rows or gene in ignore:
            continue
        segmean = segment_mean(rows, skip_low)
        if segmean is None:
            continue
        outrow = rows[0].copy()
        outrow['end'] = rows.end.iat[-1]
        outrow['gene'] = gene
        outrow['log2'] = segmean
        outrow['n_bins'] = len(rows)
        if 'weight' in rows:
            outrow['weight'] = rows['weight'].sum()
            if 'depth' in rows:
                outrow['depth'] = np.average(rows['depth'], weights=rows['weight'])
        elif 'depth' in rows:
            outrow['depth'] = rows['depth'].mean()
        yield outrow
