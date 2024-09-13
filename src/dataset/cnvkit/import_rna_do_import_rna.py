import logging
import os
import pandas as pd
from pynguin.dataset.cnvkit import rna
from pynguin.dataset.cnvkit.import_rna import aggregate_rsem, aggregate_gene_counts


def do_import_rna(gene_count_fnames, in_format, gene_resource_fname, correlations_fname=None, normal_fnames=(), do_gc=True, do_txlen=True, max_log2=3, diploid_parx_genome=None):
    """Convert a cohort of per-gene read counts to CNVkit .cnr format.

    The expected data source is TCGA gene-level expression counts for individual
    samples, but other sources should be fine, too.
    """
    gene_count_fnames = sorted(set(list(gene_count_fnames) + list(normal_fnames)))
    if in_format == 'rsem':
        (sample_counts, tx_lengths) = aggregate_rsem(gene_count_fnames)
    elif in_format == 'counts':
        sample_counts = aggregate_gene_counts(gene_count_fnames)
        tx_lengths = None
    else:
        raise RuntimeError('Unrecognized input format name: {in_format!r}')
    sample_counts = rna.filter_probes(sample_counts)
    logging.info('Loading gene metadata%s', ' and TCGA gene expression/CNV profiles' if correlations_fname else '')
    gene_info = rna.load_gene_info(gene_resource_fname, correlations_fname)
    logging.info('Aligning gene info to sample gene counts')
    normal_ids = [os.path.basename(f).split('.')[0] for f in normal_fnames]
    (gene_info, sample_counts, sample_data_log2) = rna.align_gene_info_to_samples(gene_info, sample_counts, tx_lengths, normal_ids)
    all_data = pd.concat([gene_info, sample_data_log2], axis=1)
    cnrs = rna.attach_gene_info_to_cnr(sample_counts, sample_data_log2, gene_info)
    cnrs = (rna.correct_cnr(cnr, do_gc, do_txlen, max_log2, diploid_parx_genome) for cnr in cnrs)
    return (all_data, cnrs)
