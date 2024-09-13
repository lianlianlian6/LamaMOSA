
import numpy as np

from pynguin.dataset.PEcnv.functionsInfo import group_by_genes


def gene_metrics_by_segment(cnarr, segments, threshold, skip_low=False):
    extra_cols = [col for col in segments.data.columns if col not in cnarr.data.columns and col not in ('depth', 'probes', 'weight')]
    for colname in extra_cols:
        cnarr[colname] = np.nan
    for (segment, subprobes) in cnarr.by_ranges(segments):
        if abs(segment.log2) >= threshold:
            for row in group_by_genes(subprobes, skip_low):
                row['log2'] = segment.log2
                if hasattr(segment, 'weight'):
                    row['segment_weight'] = segment.weight
                if hasattr(segment, 'probes'):
                    row['segment_probes'] = segment.probes
                for colname in extra_cols:
                    row[colname] = getattr(segment, colname)
                yield row
