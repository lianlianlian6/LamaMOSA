
from pynguin.dataset.cnvkit.antitarget import get_antitargets
from pynguin.dataset.cnvkit.params import MIN_REF_COVERAGE

def do_antitarget(targets, access=None, avg_bin_size=150000, min_bin_size=None):
    """Derive off-targt ("antitarget") bins from target regions."""
    if not min_bin_size:
        min_bin_size = 2 * int(avg_bin_size * 2 ** MIN_REF_COVERAGE)
    return get_antitargets(targets, access, avg_bin_size, min_bin_size)
