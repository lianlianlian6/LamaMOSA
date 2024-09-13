import logging
from pynguin.dataset.PEcnv import kernel, correct, measures, hyperparameters
from pynguin.dataset.PEcnv.refBaseline import shift_sex_chroms


def bias_correct_logr(cnarr, ref_columns, ref_edge_bias, ref_flat_logr, sexes, is_chr_x, is_chr_y, correct_gc, correct_edge, correct_rmask, skip_low):
    """Perform bias corrections on the sample."""
    cnarr.center_all(skip_low=skip_low)
    shift_sex_chroms(cnarr, sexes, ref_flat_logr, is_chr_x, is_chr_y)
    if (cnarr['log2'] > hyperparameters.NULL_LOG2_coverInfo - hyperparameters.MIN_REF_COVERAGE).sum() <= len(cnarr) // 2:
        logging.warning('WARNING: most bins have no or very low coverage; check that the right BED file was used')
    else:
        if 'gc' in ref_columns and correct_gc:
            cnarr = correct.center_by_window(cnarr, 0.1, ref_columns['gc'])
        if 'rmask' in ref_columns and correct_rmask:
            cnarr = correct.center_by_window(cnarr, 0.1, ref_columns['rmask'])
        if correct_edge:
            cnarr = correct.center_by_window(cnarr, 0.1, ref_edge_bias)
    return cnarr['log2']
