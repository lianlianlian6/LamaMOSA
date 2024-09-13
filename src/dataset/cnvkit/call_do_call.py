import logging
import numpy as np
from pynguin.dataset.cnvkit import segfilters
from pynguin.dataset.cnvkit.call import absolute_clonal, log2_ratios, rescale_baf, absolute_pure, absolute_threshold


def do_call(cnarr, variants=None, method='threshold', ploidy=2, purity=None, is_haploid_x_reference=False, is_sample_female=False, diploid_parx_genome=None, filters=None, thresholds=(-1.1, -0.25, 0.2, 0.7)):
    if method not in ('threshold', 'clonal', 'none'):
        raise ValueError('Argument `method` must be one of: clonal, threshold')
    outarr = cnarr.copy()
    if filters:
        for filt in ('ci', 'sem'):
            if filt in filters:
                logging.info("Applying filter '%s'", filt)
                outarr = getattr(segfilters, filt)(outarr)
                filters.remove(filt)
    if variants:
        outarr['baf'] = variants.baf_by_ranges(outarr)
    if purity and purity < 1.0:
        logging.info('Rescaling sample with purity %g, ploidy %d', purity, ploidy)
        absolutes = absolute_clonal(outarr, ploidy, purity, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
        outarr['log2'] = log2_ratios(outarr, absolutes, ploidy, is_haploid_x_reference, diploid_parx_genome)
        if variants:
            outarr['baf'] = rescale_baf(purity, outarr['baf'])
    elif method == 'clonal':
        logging.info('Calling copy number with clonal ploidy %d', ploidy)
        absolutes = absolute_pure(outarr, ploidy, is_haploid_x_reference)
    if method == 'threshold':
        tokens = ['%g => %d' % (thr, i) for (i, thr) in enumerate(thresholds)]
        logging.info('Calling copy number with thresholds: %s', ', '.join(tokens))
        absolutes = absolute_threshold(outarr, ploidy, thresholds, is_haploid_x_reference)
    if method != 'none':
        outarr['cn'] = absolutes.round().astype('int')
        if 'baf' in outarr:
            upper_baf = ((outarr['baf'] - 0.5).abs() + 0.5).fillna(1.0).values
            outarr['cn1'] = (absolutes * upper_baf).round().clip(0, outarr['cn']).astype('int')
            outarr['cn2'] = outarr['cn'] - outarr['cn1']
            is_null = outarr['baf'].isnull() & (outarr['cn'] > 0)
            outarr[is_null, 'cn1'] = np.nan
            outarr[is_null, 'cn2'] = np.nan
    if filters:
        for filt in filters:
            if not outarr.data.index.is_unique:
                logging.warning('Resetting index')
                outarr.data = outarr.data.reset_index(drop=True)
            logging.warning("Applying filter '%s'", filt)
            outarr = getattr(segfilters, filt)(outarr)
    outarr.sort_columns()
    return outarr
