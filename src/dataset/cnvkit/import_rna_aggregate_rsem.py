import os
import numpy as np
import pandas as pd
from pynguin.dataset.cnvkit import rna

def aggregate_rsem(fnames):
    """Pull out the expected read counts from each RSEM file.

    The format of RSEM's ``*_rsem.genes.results`` output files is tab-delimited
    with a header row. We extract the Ensembl gene ID, expected read counts, and
    transcript lengths from each file.

    Returns
    -------
    sample_counts : DataFrame
        Row index is Ensembl gene ID, column index is filename.
    tx_lengths : Series
        Gene lengths.
    """
    prev_row_count = None
    sample_cols = {}
    length_cols = []
    length_colname = 'length'
    for fname in fnames:
        d = pd.read_csv(fname, sep='\t', usecols=['gene_id', length_colname, 'expected_count'], converters={'gene_id': rna.before('.')}).set_index('gene_id')
        if prev_row_count is None:
            prev_row_count = len(d)
        elif len(d) != prev_row_count:
            raise RuntimeError('Number of rows in each input file is not equal')
        sample_id = rna.before('.')(os.path.basename(fname))
        sample_cols[sample_id] = d.expected_count.fillna(0)
        length_cols.append(d[length_colname])
    sample_counts = pd.DataFrame(sample_cols)
    tx_lengths = pd.Series(np.vstack(length_cols).mean(axis=0), index=sample_counts.index)
    return (sample_counts, tx_lengths)
