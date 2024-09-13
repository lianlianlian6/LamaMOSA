import logging
from pynguin.dataset.PEcnv import hyperparameters

def do_bintest(cnarr, segments=None, alpha=0.005, target_only=False):
    cnarr = cnarr.copy()
    resid = cnarr.residuals(segments)
    if not resid.index.is_unique:
        dup_idx = resid.index.duplicated(keep=False)
        logging.warning('Segments may overlap at %d bins; dropping duplicate values', dup_idx.sum())
        logging.debug('Duplicated indices: %s', ' '.join(map(str, resid[dup_idx].head(50))))
        resid = resid[~resid.index.duplicated()]
        cnarr = cnarr.as_dataframe(cnarr.data.loc[resid.index])
    if len(cnarr) != len(resid):
        logging.info('Segments do not cover all bins (%d), only %d of them', len(cnarr), len(resid))
        cnarr = cnarr.as_dataframe(cnarr.data.loc[resid.index])
    cnarr['log2'] = resid
    if target_only:
        offTarget_idx = cnarr['gene'].isin(hyperparameters.OFFTARGET_ALIASES)
        if offTarget_idx.any():
            logging.info('Ignoring %d off-target bins', offTarget_idx.sum())
            cnarr = cnarr[~offTarget_idx]
    cnarr['p_bintest'] = z_prob(cnarr)
    is_sig = cnarr['p_bintest'] < alpha
    logging.info('Significant hits in {}/{} bins ({:.3g}%)'.format(is_sig.sum(), len(is_sig), 100 * is_sig.sum() / len(is_sig)))
    hits = cnarr[is_sig]
    return hits
