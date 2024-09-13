import logging
from pynguin.dataset.PEcnv import correct, hyperparameters

def warn_bad_bins(cnarr, max_name_width=50):
    bad_bins = cnarr[correct.mask_bad_bins(cnarr)]
    fg_index = ~bad_bins['gene'].isin(hyperparameters.OFFTARGET_ALIASES)
    fg_bad_bins = bad_bins[fg_index]
    if len(fg_bad_bins) > 0:
        bad_pct = 100 * len(fg_bad_bins) / sum(~cnarr['gene'].isin(hyperparameters.OFFTARGET_ALIASES))
        if len(fg_bad_bins) < 500:
            gene_cols = min(max_name_width, max(map(len, fg_bad_bins['gene'])))
            labels = fg_bad_bins.labels()
            chrom_cols = max(labels.apply(len))
            last_gene = None
            for (label, probe) in zip(labels, fg_bad_bins):
                if probe.gene == last_gene:
                    gene = '  "'
                else:
                    gene = probe.gene
                    last_gene = gene
                if len(gene) > max_name_width:
                    gene = gene[:max_name_width - 3] + '...'
                if 'rmask' in cnarr:
                    logging.info('  %s  %s  log2=%.3f  spread=%.3f  rmask=%.3f', gene.ljust(gene_cols), label.ljust(chrom_cols), probe.log2, probe.spread, probe.rmask)
                else:
                    logging.info('  %s  %s  log2=%.3f  spread=%.3f', gene.ljust(gene_cols), label.ljust(chrom_cols), probe.log2, probe.spread)
    bg_bad_bins = bad_bins[~fg_index]
    if len(bg_bad_bins) > 0:
        bad_pct = 100 * len(bg_bad_bins) / sum(cnarr['gene'].isin(hyperparameters.OFFTARGET_ALIASES))
