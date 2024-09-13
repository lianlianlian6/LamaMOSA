
from pynguin.dataset.PEcnv.hyperparameters import MIN_REF_COVERAGE
from pynguin.dataset.PEcnv.offTarget import get_offTargets


def do_offTarget(targets, preprocess=None, avg_bin_size=150000, min_bin_size=None):
    if not min_bin_size:
        min_bin_size = 2 * int(avg_bin_size * 2 ** MIN_REF_COVERAGE)
    return get_offTargets(targets, preprocess, avg_bin_size, min_bin_size)
