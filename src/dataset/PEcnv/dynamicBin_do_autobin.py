import logging
from pynguin.dataset.PEcnv import parsingBam
from pynguin.dataset.PEcnv.dynamicBin import sample_region_cov, hybrid, update_chrom_length, average_depth


def do_autobin(bam_fname, method, targets=None, access=None, bp_per_bin=100000.0, target_min_size=20, target_max_size=50000, offTarget_min_size=500, offTarget_max_size=1000000, fasta=None):
    if method in ('amplicon', 'hybrid'):
        if targets is None:
            raise ValueError('Target regions are required for method %r but were not provided.' % method)
        if not len(targets):
            raise ValueError('Target regions are required for method %r but were not provided.' % method)

    def depth2binsize(depth, min_size, max_size):
        if depth:
            bin_size = int(round(bp_per_bin / depth))
            if bin_size < min_size:
                logging.info('Limiting est. bin size %d to given min. %d', bin_size, min_size)
                bin_size = min_size
            elif bin_size > max_size:
                logging.info('Limiting est. bin size %d to given max. %d', bin_size, max_size)
                bin_size = max_size
            return bin_size
    parsingBam.ensure_bam_index(bam_fname)
    rc_table = parsingBam.idxstats(bam_fname, drop_unmapped=True, fasta=fasta)
    read_len = parsingBam.get_read_length(bam_fname, fasta=fasta)
    logging.info('Estimated read length %s', read_len)
    if method == 'amplicon':
        tgt_depth = sample_region_cov(bam_fname, targets, fasta=fasta)
        anti_depth = None
    elif method == 'hybrid':
        (tgt_depth, anti_depth) = hybrid(rc_table, read_len, bam_fname, targets, access, fasta)
    elif method == 'wgs':
        if access is not None and len(access):
            rc_table = update_chrom_length(rc_table, access)
        tgt_depth = average_depth(rc_table, read_len)
        anti_depth = None
    tgt_bin_size = depth2binsize(tgt_depth, target_min_size, target_max_size)
    anti_bin_size = depth2binsize(anti_depth, offTarget_min_size, offTarget_max_size)
    return ((tgt_depth, tgt_bin_size), (anti_depth, anti_bin_size))
