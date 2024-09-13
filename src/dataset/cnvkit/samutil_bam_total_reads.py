from pynguin.dataset.cnvkit.samutil import idxstats


def bam_total_reads(bam_fname, fasta=None):
    """Count the total number of mapped reads in a BAM file.

    Uses the BAM index to do this quickly.
    """
    table = idxstats(bam_fname, drop_unmapped=True, fasta=fasta)
    return table.mapped.sum()
