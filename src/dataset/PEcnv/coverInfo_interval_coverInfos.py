import logging
import os.path
import time
import pandas as pd
from pynguin.dataset.PEcnv import kernel, parsingBam
from pynguin.dataset.PEcnv.cnv import CopyNumArray as CNA
from pynguin.dataset.PEcnv.coverInfo import interval_coverInfos_count, interval_coverInfos_pileup


def interval_coverInfos(bed_fname, bam_fname, by_count, min_mapq, processes, fasta=None):
    meta = {'sample_id': kernel.fbase(bam_fname)}
    start_time = time.time()
    with open(bed_fname) as bed_handle:
        for line in bed_handle:
            if line.strip():
                break
        else:
            logging.info('Skip processing %s with empty regions file %s', os.path.basename(bam_fname), bed_fname)
            return CNA.from_rows([], meta_dict=meta)
    if by_count:
        results = interval_coverInfos_count(bed_fname, bam_fname, min_mapq, processes, fasta)
        (read_counts, cna_rows) = zip(*results)
        read_counts = pd.Series(read_counts)
        cnarr = CNA.from_rows(list(cna_rows), columns=CNA._required_columns + ('depth',), meta_dict=meta)
    else:
        table = interval_coverInfos_pileup(bed_fname, bam_fname, min_mapq, processes, fasta)
        read_len = parsingBam.get_read_length(bam_fname, fasta=fasta)
        read_counts = table['basecount'] / read_len
        table = table.drop('basecount', axis=1)
        cnarr = CNA(table, meta)
    tot_time = time.time() - start_time
    tot_reads = read_counts.sum()
    tot_mapped_reads = parsingBam.bam_total_reads(bam_fname, fasta=fasta)
    if tot_mapped_reads:
        logging.info('Percent reads in regions: %.3f (of %d mapped)', 100.0 * tot_reads / tot_mapped_reads, tot_mapped_reads)
    else:
        logging.info("(Couldn't calculate total number of mapped reads)")
    return cnarr
