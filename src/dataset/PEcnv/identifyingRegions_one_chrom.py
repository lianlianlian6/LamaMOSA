from __future__ import division
import logging
import pandas as pd

from pynguin.dataset.PEcnv.identifyingRegions import PE_haar


def one_chrom(cnarr, fdr_q, chrom):
    logging.debug('Segmenting %s', chrom)
    results = PE_haar(cnarr.smooth_log2(), fdr_q, W=cnarr['weight'].values if 'weight' in cnarr else None)
    print(results)
    table = pd.DataFrame({'chromosome': chrom, 'start': cnarr['start'].values.take(results['start']), 'end': cnarr['end'].values.take(results['end']), 'log2': results['mean'], 'gene': '-', 'probes': results['size']})
    return table
