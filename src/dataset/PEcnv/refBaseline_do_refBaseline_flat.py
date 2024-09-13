import logging
import numpy as np

def do_refBaseline_flat(targets, offTargets=None, fa_fname=None, male_refBaseline=False):
    ref_probes = bed2probes(targets)
    if offTargets:
        ref_probes.add(bed2probes(offTargets))
    ref_probes['log2'] = ref_probes.expect_flat_log2(male_refBaseline)
    ref_probes['depth'] = np.exp2(ref_probes['log2'])
    if fa_fname:
        (gc, rmask) = get_fasta_stats(ref_probes, fa_fname)
        ref_probes['gc'] = gc
        ref_probes['rmask'] = rmask
    else:
        logging.info('No FASTA refBaseline genome provided; skipping GC, RM calculations')
    ref_probes.sort_columns()
    return ref_probes
