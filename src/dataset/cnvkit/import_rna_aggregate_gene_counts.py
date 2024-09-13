import os
import pandas as pd
from pynguin.dataset.cnvkit import rna

def aggregate_gene_counts(filenames):
    prev_row_count = None
    sample_cols = {}
    for fname in filenames:
        d = pd.read_csv(fname, sep='\t', comment='_', header=None, names=['gene_id', 'expected_count'], converters={'gene_id': rna.before('.')}).set_index('gene_id')
        if prev_row_count is None:
            prev_row_count = len(d)
        elif len(d) != prev_row_count:
            raise RuntimeError('Number of rows in each input file is not equal')
        sample_id = rna.before('.')(os.path.basename(fname))
        sample_cols[sample_id] = d.expected_count.fillna(0)
    sample_counts = pd.DataFrame(sample_cols)
    return sample_counts
