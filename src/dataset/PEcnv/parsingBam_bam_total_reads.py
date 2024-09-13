from pynguin.dataset.PEcnv.parsingBam import idxstats


def bam_total_reads(bam_fname, fasta=None):
    table = idxstats(bam_fname, drop_unmapped=True, fasta=fasta)
    return table.mapped.sum()
