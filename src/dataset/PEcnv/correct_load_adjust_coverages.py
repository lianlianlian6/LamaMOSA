import logging

from pynguin.dataset.PEcnv import hyperparameters
from pynguin.dataset.PEcnv.correct import mask_bad_bins, match_ref_to_sample, center_by_window, get_edge_bias


def load_adjust_coverages(cnarr, ref_cnarr, skip_low, correct_gc, correct_edge, correct_rmask):
    if 'gc' in cnarr:
        cnarr = cnarr.keep_columns(cnarr._required_columns + ('depth',))
    if not len(cnarr):
        return (cnarr, ref_cnarr[:0])
    ref_matched = match_ref_to_sample(ref_cnarr, cnarr)
    ok_cvg_indices = ~mask_bad_bins(ref_matched)
    cnarr = cnarr[ok_cvg_indices]
    ref_matched = ref_matched[ok_cvg_indices]
    if (cnarr['log2'] > hyperparameters.NULL_LOG2_coverInfo - hyperparameters.MIN_REF_COVERAGE).sum() <= len(cnarr) // 2:
        logging.warning('WARNING: most bins have no or very low coverage; check that the right BED file was used')
    else:
        cnarr_index_reset = False
        if correct_gc:
            if 'gc' in ref_matched:
                logging.info('Correcting for GC bias...')
                cnarr = center_by_window(cnarr, 0.1, ref_matched['gc'])
                cnarr_index_reset = True
            else:
                logging.warning('WARNING: Skipping correction for GC bias')
        if correct_edge:
            logging.info('Correcting for density bias...')
            edge_bias = get_edge_bias(cnarr, hyperparameters.INSERT_SIZE)
            cnarr = center_by_window(cnarr, 0.1, edge_bias)
            cnarr_index_reset = True
        if correct_rmask:
            if 'rmask' in ref_matched:
                logging.info('Correcting for RepeatMasker bias...')
                cnarr = center_by_window(cnarr, 0.1, ref_matched['rmask'])
                cnarr_index_reset = True
            else:
                logging.warning('WARNING: Skipping correction for RepeatMasker bias')
        if cnarr_index_reset:
            ref_matched.data.reset_index(drop=True, inplace=True)
    return (cnarr, ref_matched)
