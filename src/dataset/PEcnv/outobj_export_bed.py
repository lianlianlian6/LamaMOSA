from pynguin.dataset.PEcnv import finalcall

def export_bed(segments, ploidy, is_reference_male, is_sample_female, label, show):
    out = segments.data.reindex(columns=['chromosome', 'start', 'end'])
    out['label'] = label if label else segments['gene']
    out['ncopies'] = segments['cn'] if 'cn' in segments else finalcall.absolute_pure(segments, ploidy, is_reference_male).round().astype('int')
    if show == 'ploidy':
        out = out[out['ncopies'] != ploidy]
    elif show == 'variant':
        exp_copies = finalcall.absolute_expect(segments, ploidy, is_sample_female)
        out = out[out['ncopies'] != exp_copies]
    return out
