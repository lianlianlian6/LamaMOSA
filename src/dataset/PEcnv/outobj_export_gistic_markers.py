import pandas as pd
from pynguin.dataset.PEcnv.implementation import read_cna

def export_gistic_markers(cnr_fnames):
    colnames = ['ID', 'CHROM', 'POS']
    out_chunks = []
    for fname in cnr_fnames:
        cna = read_cna(fname).autosomes()
        marker_ids = cna.labels()
        tbl = pd.concat([pd.DataFrame({'ID': marker_ids, 'CHROM': cna.chromosome, 'POS': cna.start + 1}, columns=colnames), pd.DataFrame({'ID': marker_ids, 'CHROM': cna.chromosome, 'POS': cna.end}, columns=colnames)], ignore_index=True)
        out_chunks.append(tbl)
    return pd.concat(out_chunks).drop_duplicates()
