import numpy as np

from pynguin.dataset.PEcnv.refBaseline import calculate_gc_lo, fasta_extract_regions


def get_fasta_stats(cnarr, fa_fname):
    gc_rm_vals = [calculate_gc_lo(subseq) for subseq in fasta_extract_regions(fa_fname, cnarr)]
    (gc_vals, rm_vals) = zip(*gc_rm_vals)
    return (np.asfarray(gc_vals), np.asfarray(rm_vals))
