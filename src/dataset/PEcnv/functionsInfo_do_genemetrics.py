import pandas as pd

from pynguin.dataset.PEcnv.functionsInfo import gene_metrics_by_segment, gene_metrics_by_gene


def do_genemetrics(cnarr, segments=None, threshold=0.2, min_probes=3, skip_low=False, male_reference=False, is_sample_female=None):
    if is_sample_female is None:
        is_sample_female = cnarr.guess_xx(male_reference=male_reference)
    cnarr = cnarr.shift_xx(male_reference, is_sample_female)
    if segments:
        segments = segments.shift_xx(male_reference, is_sample_female)
        rows = gene_metrics_by_segment(cnarr, segments, threshold, skip_low)
    else:
        rows = gene_metrics_by_gene(cnarr, threshold, skip_low)
    rows = list(rows)
    columns = rows[0].index if len(rows) else cnarr._required_columns
    columns = ['gene'] + [col for col in columns if col != 'gene']
    table = pd.DataFrame.from_records(rows).reindex(columns=columns)
    if min_probes and len(table):
        n_probes = table.segment_probes if 'segment_probes' in table.columns else table.n_bins
        table = table[n_probes >= min_probes]
    return table
