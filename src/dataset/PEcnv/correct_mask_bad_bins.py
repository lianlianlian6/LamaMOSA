from pynguin.dataset.PEcnv import hyperparameters


def mask_bad_bins(cnarr):
    mask = (cnarr['log2'] < hyperparameters.MIN_REF_COVERAGE) | (cnarr['log2'] > -hyperparameters.MIN_REF_COVERAGE) | (cnarr['spread'] > hyperparameters.MAX_REF_SPREAD)
    if 'depth' in cnarr:
        mask |= cnarr['depth'] == 0
    if 'gc' in cnarr:
        mask |= (cnarr['gc'] > 0.7) | (cnarr['gc'] < 0.3)
    return mask
