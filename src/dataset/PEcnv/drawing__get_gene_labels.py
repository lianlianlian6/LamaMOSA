from pynguin.dataset.PEcnv import hyperparameters, functionsInfo

def _get_gene_labels(cnarr, segarr, cnarr_is_seg, threshold, min_probes):
    if cnarr_is_seg:
        sel = cnarr.data[(cnarr.data.log2.abs() >= threshold) & ~cnarr.data.gene.isin(hyperparameters.IGNORE_GENE_NAMES)]
        rows = sel.itertuples(index=False)
        probes_attr = 'probes'
    elif segarr:
        rows = functionsInfo.gene_metrics_by_segment(cnarr, segarr, threshold)
        probes_attr = 'segment_probes'
    else:
        rows = functionsInfo.gene_metrics_by_gene(cnarr, threshold)
        probes_attr = 'n_bins'
    return [row.gene for row in rows if getattr(row, probes_attr) >= min_probes]
