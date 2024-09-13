import logging
from pynguin.dataset.cnvkit import params
from pynguin.dataset.cnvkit.fix import match_ref_to_sample, mask_bad_bins, center_by_window, get_edge_bias


def load_adjust_coverages(cnarr, ref_cnarr, skip_low, fix_gc, fix_edge, fix_rmask, diploid_parx_genome, smoothing_window_fraction=None):
    """Load and filter probe coverages; correct using reference and GC."""
    if 'gc' in cnarr:
        cnarr = cnarr.keep_columns(cnarr._required_columns + ('depth',))
    if not len(cnarr):
        return (cnarr, ref_cnarr[:0])
    ref_matched = match_ref_to_sample(ref_cnarr, cnarr)
    ok_cvg_indices = ~mask_bad_bins(ref_matched)
    logging.info('Keeping %d of %d bins', sum(ok_cvg_indices), len(ref_matched))
    cnarr = cnarr[ok_cvg_indices]
    ref_matched = ref_matched[ok_cvg_indices]
    cnarr.center_all(skip_low=skip_low, diploid_parx_genome=diploid_parx_genome)
    if (cnarr['log2'] > params.NULL_LOG2_COVERAGE - params.MIN_REF_COVERAGE).sum() <= len(cnarr) // 2:
        logging.warning('WARNING: most bins have no or very low coverage; check that the right BED file was used')
    else:
        frac = smoothing_window_fraction
        if frac is None:
            frac = max(0.01, len(cnarr) ** (-0.5))
        cnarr_index_reset = False
        if fix_gc:
            if 'gc' in ref_matched:
                logging.info('Correcting for GC bias...')
                cnarr = center_by_window(cnarr, frac, ref_matched['gc'])
                cnarr_index_reset = True
            else:
                logging.warning('WARNING: Skipping correction for GC bias')
        if fix_edge:
            logging.info('Correcting for density bias...')
            edge_bias = get_edge_bias(cnarr, params.INSERT_SIZE)
            cnarr = center_by_window(cnarr, frac, edge_bias)
            cnarr_index_reset = True
        if fix_rmask:
            if 'rmask' in ref_matched:
                logging.info('Correcting for RepeatMasker bias...')
                cnarr = center_by_window(cnarr, frac, ref_matched['rmask'])
                cnarr_index_reset = True
            else:
                logging.warning('WARNING: Skipping correction for RepeatMasker bias')
        if cnarr_index_reset:
            ref_matched.data.reset_index(drop=True, inplace=True)
    return (cnarr, ref_matched)
