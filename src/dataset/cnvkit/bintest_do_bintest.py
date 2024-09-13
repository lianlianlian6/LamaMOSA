import logging
from pynguin.dataset.cnvkit import params
from pynguin.dataset.cnvkit.bintest import z_prob


def do_bintest(cnarr, segments=None, alpha=0.005, target_only=False):
    """Get a probability for each bin based on its Z-score.

    Adds a column w/ p-values to the input .cnr. With `segments`, the Z-score is
    relative to the enclosing segment's mean, otherwise it is relative to 0.

    Bin p-values are corrected for multiple hypothesis testing by the
    Benjamini-Hochberg method.

    Returns: bins where the probability < `alpha`.
    """
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
    cnarr['probes'] = 1
    if target_only:
        antitarget_idx = cnarr['gene'].isin(params.ANTITARGET_ALIASES)
        if antitarget_idx.any():
            logging.info('Ignoring %d off-target bins', antitarget_idx.sum())
            cnarr = cnarr[~antitarget_idx]
    cnarr['p_bintest'] = z_prob(cnarr)
    is_sig = cnarr['p_bintest'] < alpha
    logging.info('Significant hits in {}/{} bins ({:.3g}%)'.format(is_sig.sum(), len(is_sig), 100 * is_sig.sum() / len(is_sig)))
    hits = cnarr[is_sig]
    return hits
