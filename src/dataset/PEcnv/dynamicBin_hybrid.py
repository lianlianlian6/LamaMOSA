from pynguin.dataset.PEcnv.dynamicBin import idxstats2ga, shared_chroms, sample_region_cov, region_size_by_chrom, \
    update_chrom_length, average_depth
from pynguin.dataset.PEcnv.offTarget import compare_chrom_names

def hybrid(rc_table, read_len, bam_fname, targets, access=None, fasta=None):
    if access is None:
        access = idxstats2ga(rc_table, bam_fname)
        compare_chrom_names(access, targets)
    offTargets = access.subtract(targets)
    (rc_table, targets, offTargets) = shared_chroms(rc_table, targets, offTargets)
    target_depth = sample_region_cov(bam_fname, targets, fasta=fasta)
    target_length = region_size_by_chrom(targets)['length']
    target_reads = (target_length * target_depth / read_len).values
    anti_table = update_chrom_length(rc_table, offTargets)
    anti_table = anti_table.assign(mapped=anti_table.mapped - target_reads)
    anti_depth = average_depth(anti_table, read_len)
    return (target_depth, anti_depth)
