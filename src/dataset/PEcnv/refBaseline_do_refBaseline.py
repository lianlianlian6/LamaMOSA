import collections
import logging
from pynguin.dataset.PEcnv import kernel
from pynguin.dataset.PEcnv.refBaseline import infer_sexes, combine_probes, warn_bad_bins


def do_refBaseline(target_fnames, offTarget_fnames=None, fa_fname=None, male_refBaseline=False, female_samples=None, do_gc=True, do_edge=True, do_rmask=True, do_cluster=False, min_cluster_size=4):
    if offTarget_fnames:
        kernel.assert_equal('Unequal number of target and offTarget files given', targets=len(target_fnames), offTargets=len(offTarget_fnames))
    if not fa_fname:
        logging.info('No FASTA refBaseline genome provided; skipping GC, RM calculations')
    if female_samples is None:
        sexes = infer_sexes(target_fnames, False)
        if offTarget_fnames:
            a_sexes = infer_sexes(offTarget_fnames, False)
            for (sid, a_is_xx) in a_sexes.items():
                t_is_xx = sexes.get(sid)
                if t_is_xx is None:
                    sexes[sid] = a_is_xx
                elif t_is_xx != a_is_xx and a_is_xx is not None:
                    sexes[sid] = a_is_xx
    else:
        sexes = collections.defaultdict(lambda : female_samples)
    ref_probes = combine_probes(target_fnames, offTarget_fnames, fa_fname, male_refBaseline, sexes, do_gc, do_edge, do_rmask, do_cluster, min_cluster_size)
    warn_bad_bins(ref_probes)
    return ref_probes
