from concurrent import futures
import numpy as np
import pandas as pd

from .coverInfo import bedcov, _bedcov
from .multiprocess import rm, to_chunks
from .hyperparameters import NULL_LOG2_coverInfo

def interval_coverInfos_pileup(bed_fname, bam_fname, min_mapq, procs=1, fasta=None):
    if procs == 1:
        table = bedcov(bed_fname, bam_fname, min_mapq, fasta)
    else:
        chunks = []
        with futures.ProcessPoolExecutor(procs) as pool:
            args_iter = ((bed_chunk, bam_fname, min_mapq, fasta) for bed_chunk in to_chunks(bed_fname))
            for (bed_chunk_fname, table) in pool.map(_bedcov, args_iter):
                chunks.append(table)
                rm(bed_chunk_fname)
        table = pd.concat(chunks, ignore_index=True)
    if 'gene' in table:
        table['gene'] = table['gene'].fillna('-')
    else:
        table['gene'] = '-'
    spans = table.end - table.start
    ok_idx = spans > 0
    table = table.assign(depth=0, log2=NULL_LOG2_coverInfo)
    table.loc[ok_idx, 'depth'] = table.loc[ok_idx, 'basecount'] / spans[ok_idx]
    ok_idx = table['depth'] > 0
    table.loc[ok_idx, 'log2'] = np.log2(table.loc[ok_idx, 'depth'])
    return table
