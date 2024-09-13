from __future__ import division
import logging
import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.identifyingRegions import haarSeg


def variants_in_segment(varr, segment, fdr_q):
    if len(varr):
        values = varr.mirrored_baf(above_half=True, tumor_boost=True)
        results = haarSeg(values, fdr_q, W=None)
    else:
        values = pd.Series()
        results = None
    if results is not None and len(results['start']) > 1:
        logging.info('Segmented on allele freqs in %s:%d-%d', segment.chromosome, segment.start, segment.end)
        gap_rights = varr['start'].values.take(results['start'][1:])
        gap_lefts = varr['end'].values.take(results['end'][:-1])
        mid_breakpoints = (gap_lefts + gap_rights) // 2
        starts = np.concatenate([[segment.start], mid_breakpoints])
        ends = np.concatenate([mid_breakpoints, [segment.end]])
        table = pd.DataFrame({'chromosome': segment.chromosome, 'start': starts, 'end': ends, 'gene': segment.gene, 'log2': segment.log2, 'probes': results['size']})
    else:
        table = pd.DataFrame({'chromosome': segment.chromosome, 'start': segment.start, 'end': segment.end, 'gene': segment.gene, 'log2': segment.log2, 'probes': segment.probes}, index=[0])
    return table
