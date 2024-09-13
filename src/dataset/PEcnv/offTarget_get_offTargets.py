from pynguin.dataset.PEcnv.hyperparameters import INSERT_SIZE, OFFTARGET_NAME
from pynguin.dataset.PEcnv.offTarget import drop_noncanonical_contigs, guess_chromosome_regions


def get_offTargets(targets, preprocessible, avg_bin_size, min_bin_size):
    if preprocessible:
        preprocessible = drop_noncanonical_contigs(preprocessible, targets)
    else:
        TELOMERE_SIZE = 150000
        preprocessible = guess_chromosome_regions(targets, TELOMERE_SIZE)
    pad_size = 2 * INSERT_SIZE
    bg_arr = preprocessible.resize_ranges(-pad_size).subtract(targets.resize_ranges(pad_size)).subdivide(avg_bin_size, min_bin_size)
    bg_arr['gene'] = OFFTARGET_NAME
    return bg_arr
