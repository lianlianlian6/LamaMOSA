import math
from pynguin.dataset.PEcnv.hyperparameters import NULL_LOG2_coverInfo

def region_depth_count(bamfile, chrom, start, end, gene, min_mapq):

    def filter_read(read):
        return not (read.is_duplicate or read.is_secondary or read.is_unmapped or read.is_qcfail or (read.mapq < min_mapq))
    count = 0
    bases = 0
    for read in bamfile.fetch(reference=chrom, start=start, end=end):
        if filter_read(read):
            count += 1
            rlen = read.query_alignment_length
            if read.pos < start:
                rlen -= start - read.pos
            if read.pos + read.query_alignment_length > end:
                rlen -= read.pos + read.query_alignment_length - end
            bases += rlen
    depth = bases / (end - start) if end > start else 0
    row = (chrom, start, end, gene, math.log(depth, 2) if depth else NULL_LOG2_coverInfo, depth)
    return (count, row)
