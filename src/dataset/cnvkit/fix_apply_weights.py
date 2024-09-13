import logging
import numpy as np
from pynguin.dataset.cnvkit import descriptives, params

def apply_weights(cnarr, ref_matched, log2_key, spread_key, epsilon=0.0001):
    """Calculate weights for each bin.

    Bin weight is an estimate of (1 - variance) and within the range
    ``(0, 1]``.

    Weights are derived from:

    - Each bin's size
    - Sample's genome-wide average (on/off-target) coverage depth
    - Sample's genome-wide observed (on/off-target) bin variances

    And with a pooled reference:

    - Each bin's coverage depth in the reference
    - The "spread" column of the reference (approx. stdev)

    These estimates of variance assume the number of aligned reads per bin
    follows a Poisson distribution, approximately log-normal.

    Parameters
    ----------
    cnarr : CopyNumArray
        Sample bins.
    ref_match : CopyNumArray
        Reference bins.
    log2_key : string
        The 'log2' column name in the reference to use. A clustered reference
        may have a suffix indicating the cluster, e.g. "log2_1".
    spread_key : string
        The 'spread' or 'spread_<cluster_id>' column name to use.
    epsilon : float
        Minimum value for bin weights, to avoid 0-weight bins causing errors
        later during segmentation. (CBS doesn't allow 0-weight bins.)

    Returns: The input `cnarr` with a `weight` column added.
    """
    logging.debug('Weighting bins by size and overall variance in sample')
    simple_wt = np.zeros(len(cnarr))
    is_anti = cnarr['gene'].isin(params.ANTITARGET_ALIASES)
    tgt_cna = cnarr[~is_anti]
    tgt_var = descriptives.biweight_midvariance(tgt_cna.drop_low_coverage().residuals()) ** 2
    bin_sz = np.sqrt(tgt_cna['end'] - tgt_cna['start'])
    tgt_simple_wts = 1 - tgt_var / (bin_sz / bin_sz.mean())
    simple_wt[~is_anti] = tgt_simple_wts
    if is_anti.any():
        anti_cna = cnarr[is_anti]
        anti_ok = anti_cna.drop_low_coverage()
        frac_anti_low = 1 - len(anti_ok) / len(anti_cna)
        if frac_anti_low > 0.5:
            logging.warning('WARNING: Most antitarget bins ({:.2f}%, {:d}/{:d}) have low or no coverage; is this amplicon/WGS?'.format(100 * frac_anti_low, len(anti_cna) - len(anti_ok), len(anti_cna)))
        anti_var = descriptives.biweight_midvariance(anti_ok.residuals()) ** 2
        anti_bin_sz = np.sqrt(anti_cna['end'] - anti_cna['start'])
        anti_simple_wts = 1 - anti_var / (anti_bin_sz / anti_bin_sz.mean())
        simple_wt[is_anti] = anti_simple_wts
        var_ratio = max(tgt_var, 0.01) / max(anti_var, 0.01)
        if var_ratio > 1:
            logging.info('Targets are %.2f x more variable than antitargets', var_ratio)
        else:
            logging.info('Antitargets are %.2f x more variable than targets', 1.0 / var_ratio)
    if (ref_matched[spread_key] > epsilon).any() and (np.abs(np.mod(ref_matched[log2_key], 1)) > epsilon).any():
        logging.debug('Weighting bins by coverage spread in reference')
        fancy_wt = 1.0 - ref_matched[spread_key] ** 2
        x = 0.9
        weights = x * fancy_wt + (1 - x) * simple_wt
    else:
        weights = simple_wt
    return cnarr.add_columns(weight=weights.clip(epsilon, 1.0))
