import numpy as np

from pynguin.dataset.PEcnv.formats import parse_theta_results


def do_import_theta(segarr, theta_results_fname, ploidy=2):
    theta = parse_theta_results(theta_results_fname)
    segarr = segarr.autosomes()
    for copies in theta['C']:
        if len(copies) != len(segarr):
            copies = copies[:len(segarr)]
        mask_drop = np.array([c is None for c in copies], dtype='bool')
        segarr = segarr[~mask_drop].copy()
        ok_copies = np.asfarray([c for c in copies if c is not None])
        segarr['cn'] = ok_copies.astype('int')
        ok_copies[ok_copies == 0] = 0.5
        segarr['log2'] = np.log2(ok_copies / ploidy)
        segarr.sort_columns()
        yield segarr
