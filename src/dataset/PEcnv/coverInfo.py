import logging
import math
import os.path
import time
from concurrent import futures

import numpy as np
import pandas as pd
# import pysam
from io import StringIO
# from pegeno import tabio

from pynguin.dataset.PEcnv import kernel, parsingBam
# from pynguin.dataset.PEcnv.cnv import CopyNumArray as CNA
from pynguin.dataset.PEcnv.multiprocess import rm, to_chunks
from pynguin.dataset.PEcnv.hyperparameters import NULL_LOG2_coverInfo


def do_coverInfo(bed_fname, bam_fname, by_count=False, min_mapq=0, processes=1, fasta=None):
    if not parsingBam.ensure_bam_sorted(bam_fname, fasta=fasta):
        raise RuntimeError("BAM file %s must be sorted by coordinates"
                           % bam_fname)
    parsingBam.ensure_bam_index(bam_fname)

    cnarr = interval_coverInfos(bed_fname, bam_fname, by_count, min_mapq,
                                processes, fasta)
    return cnarr


def interval_coverInfos(bed_fname, bam_fname, by_count, min_mapq, processes, fasta=None):
    meta = {'sample_id': kernel.fbase(bam_fname)}
    start_time = time.time()

    with open(bed_fname) as bed_handle:
        for line in bed_handle:
            if line.strip():
                break
        else:
            logging.info("Skip processing %s with empty regions file %s",
                         os.path.basename(bam_fname), bed_fname)
            return CNA.from_rows([], meta_dict=meta)

    if by_count:
        results = interval_coverInfos_count(bed_fname, bam_fname, min_mapq,
                                            processes, fasta)
        read_counts, cna_rows = zip(*results)
        read_counts = pd.Series(read_counts)
        cnarr = CNA.from_rows(list(cna_rows),
                              columns=CNA._required_columns + ('depth',),
                              meta_dict=meta)
    else:
        table = interval_coverInfos_pileup(bed_fname, bam_fname, min_mapq,
                                           processes, fasta)
        read_len = parsingBam.get_read_length(bam_fname, fasta=fasta)
        read_counts = table['basecount'] / read_len
        table = table.drop('basecount', axis=1)
        cnarr = CNA(table, meta)

    tot_time = time.time() - start_time
    tot_reads = read_counts.sum()

    tot_mapped_reads = parsingBam.bam_total_reads(bam_fname, fasta=fasta)
    if tot_mapped_reads:
        logging.info("Percent reads in regions: %.3f (of %d mapped)",
                     100. * tot_reads / tot_mapped_reads,
                     tot_mapped_reads)
    else:
        logging.info("(Couldn't calculate total number of mapped reads)")

    return cnarr


def interval_coverInfos_count(bed_fname, bam_fname, min_mapq, procs=1, fasta=None):
    regions = tabio.read_auto(bed_fname)
    if procs == 1:
        bamfile = pysam.Samfile(bam_fname, 'rb', reference_filename=fasta)
        for chrom, subregions in regions.by_chromosome():

            for count, row in _rdc_chunk(bamfile, subregions, min_mapq):
                yield [count, row]
    else:
        with futures.ProcessPoolExecutor(procs) as pool:
            args_iter = ((bam_fname, subr, min_mapq, fasta)
                         for _c, subr in regions.by_chromosome())
            for chunk in pool.map(_rdc, args_iter):
                for count, row in chunk:
                    yield [count, row]


def _rdc(args):
    """Wrapper for parallel."""
    return list(_rdc_chunk(*args))


def _rdc_chunk(bamfile, regions, min_mapq, fasta=None):
    if isinstance(bamfile, str):
        bamfile = pysam.Samfile(bamfile, 'rb', reference_filename=fasta)
    for chrom, start, end, gene in regions.coords(["gene"]):
        yield region_depth_count(bamfile, chrom, start, end, gene, min_mapq)


def region_depth_count(bamfile, chrom, start, end, gene, min_mapq):
    def filter_read(read):

        return not (read.is_duplicate
                    or read.is_secondary
                    or read.is_unmapped
                    or read.is_qcfail
                    or read.mapq < min_mapq)

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
    row = (chrom, start, end, gene,
           math.log(depth, 2) if depth else NULL_LOG2_coverInfo,
           depth)
    return count, row


def interval_coverInfos_pileup(bed_fname, bam_fname, min_mapq, procs=1, fasta=None):
    if procs == 1:
        table = bedcov(bed_fname, bam_fname, min_mapq, fasta)
    else:
        chunks = []
        with futures.ProcessPoolExecutor(procs) as pool:
            args_iter = ((bed_chunk, bam_fname, min_mapq, fasta)
                         for bed_chunk in to_chunks(bed_fname))
            for bed_chunk_fname, table in pool.map(_bedcov, args_iter):
                chunks.append(table)
                rm(bed_chunk_fname)
        table = pd.concat(chunks, ignore_index=True)

    if 'gene' in table:
        table['gene'] = table['gene'].fillna('-')
    else:
        table['gene'] = '-'

    spans = table.end - table.start
    ok_idx = (spans > 0)
    table = table.assign(depth=0, log2=NULL_LOG2_coverInfo)
    table.loc[ok_idx, 'depth'] = (table.loc[ok_idx, 'basecount']
                                  / spans[ok_idx])
    ok_idx = (table['depth'] > 0)
    table.loc[ok_idx, 'log2'] = np.log2(table.loc[ok_idx, 'depth'])
    return table


def _bedcov(args):
    bed_fname = args[0]
    table = bedcov(*args)
    return bed_fname, table


def bedcov(bed_fname, bam_fname, min_mapq, fasta=None):
    cmd = [bed_fname, bam_fname]
    if min_mapq and min_mapq > 0:
        cmd.extend(['-Q', bytes(min_mapq)])
    if fasta:
        cmd.extend(['--reference', fasta])
    try:
        raw = pysam.bedcov(*cmd, split_lines=False)
    except pysam.SamtoolsError as exc:
        raise ValueError("Failed processing %r coverInfos in %r regions. "
                         "PySAM error: %s" % (bam_fname, bed_fname, exc))
    if not raw:
        raise ValueError("BED file %r chromosome names don't match any in "
                         "BAM file %r" % (bed_fname, bam_fname))
    columns = detect_bedcov_columns(raw)
    table = pd.read_csv(StringIO(raw), sep='\t', names=columns, usecols=columns)
    return table


def detect_bedcov_columns(text):
    firstline = text[:text.index('\n')]
    tabcount = firstline.count('\t')
    if tabcount < 3:
        raise RuntimeError("Bad line from bedcov:\n%r" % firstline)
    if tabcount == 3:
        return ['chromosome', 'start', 'end', 'basecount']
    if tabcount == 4:
        return ['chromosome', 'start', 'end', 'gene', 'basecount']

    fillers = ["_%d" % i for i in range(1, tabcount - 3)]
    return ['chromosome', 'start', 'end', 'gene'] + fillers + ['basecount']
