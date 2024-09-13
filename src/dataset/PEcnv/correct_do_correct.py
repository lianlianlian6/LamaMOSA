import logging
import numpy as np

from pynguin.dataset.PEcnv.correct import load_adjust_coverages, apply_weights


def do_correct(target_raw, offTarget_raw, reference, do_gc=True, do_edge=True, do_rmask=True, do_cluster=False):
    logging.info('Processing target: %s', target_raw.sample_id)
    (cnarr, ref_matched) = load_adjust_coverages(target_raw, reference, True, do_gc, do_edge, False)
    logging.info('Processing offTarget: %s', offTarget_raw.sample_id)
    (anti_cnarr, ref_anti) = load_adjust_coverages(offTarget_raw, reference, False, do_gc, False, do_rmask)
    if len(anti_cnarr):
        cnarr.add(anti_cnarr)
        ref_matched.add(ref_anti)
    log2_key = 'log2'
    spread_key = 'spread'
    if do_cluster:
        ref_log2_cols = [col for col in ref_matched.data.columns if col == 'log2' or col.startswith('log2')]
        if len(ref_log2_cols) == 1:
            logging.info('Reference does not contain any sub-clusters; using %s', log2_key)
        else:
            corr_coefs = np.array([cnarr.log2.corr(ref_matched[ref_col]) for ref_col in ref_log2_cols])
            ordered = [(k, r) for (r, k) in sorted(zip(corr_coefs, ref_log2_cols), reverse=True)]
            logging.info('Correlations with each cluster:\n\t%s', '\n\t'.join(['{}\t: {}'.format(k, r) for (k, r) in ordered]))
            log2_key = ordered[0][0]
            if log2_key.startswith('log2_'):
                sufcorrect = log2_key.split('_', 1)[1]
                spread_key = 'spread_' + sufcorrect
            logging.info(' -> Choosing columns %r and %r', log2_key, spread_key)
    cnarr.data['log2'] -= ref_matched[log2_key]
    cnarr = apply_weights(cnarr, ref_matched, log2_key, spread_key)
    cnarr.center_all(skip_low=True)
    return cnarr
