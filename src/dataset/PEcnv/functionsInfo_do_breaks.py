
import pandas as pd

from pynguin.dataset.PEcnv.functionsInfo import get_gene_intervals, get_breakpoints


def do_breaks(probes, segments, min_probes=1):
    intervals = get_gene_intervals(probes)
    bpoints = get_breakpoints(intervals, segments, min_probes)
    return pd.DataFrame.from_records(bpoints, columns=['gene', 'chromosome', 'location', 'change', 'probes_left', 'probes_right'])
