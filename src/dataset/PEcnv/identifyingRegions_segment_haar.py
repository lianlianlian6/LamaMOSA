from __future__ import division
import pandas as pd

from pynguin.dataset.PEcnv.identifyingRegions import one_chrom


def segment_haar(cnarr, fdr_q):
    chrom_tables = [one_chrom(subprobes, fdr_q, chrom) for (chrom, subprobes) in cnarr.by_arm()]
    segarr = cnarr.as_dataframe(pd.concat(chrom_tables))
    segarr.sort_columns()
    return segarr
