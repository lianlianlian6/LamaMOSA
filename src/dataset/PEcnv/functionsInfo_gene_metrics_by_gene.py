from pynguin.dataset.PEcnv.functionsInfo import group_by_genes


def gene_metrics_by_gene(cnarr, threshold, skip_low=False):
    for row in group_by_genes(cnarr, skip_low):
        if abs(row.log2) >= threshold and row.gene:
            yield row
