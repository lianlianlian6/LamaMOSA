from pynguin.dataset.PEcnv import parsingBam
from pynguin.dataset.PEcnv.coverInfo import interval_coverInfos


def do_coverInfo(bed_fname, bam_fname, by_count=False, min_mapq=0, processes=1, fasta=None):
    if not parsingBam.ensure_bam_sorted(bam_fname, fasta=fasta):
        raise RuntimeError('BAM file %s must be sorted by coordinates' % bam_fname)
    parsingBam.ensure_bam_index(bam_fname)
    cnarr = interval_coverInfos(bed_fname, bam_fname, by_count, min_mapq, processes, fasta)
    return cnarr
