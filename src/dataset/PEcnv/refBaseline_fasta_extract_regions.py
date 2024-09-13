import pyfaidx

def fasta_extract_regions(fa_fname, intervals):
    with pyfaidx.Fasta(fa_fname, as_raw=True) as fa_file:
        for (chrom, subarr) in intervals.by_chromosome():
            for (_chrom, start, end) in subarr.coords():
                yield fa_file[_chrom][int(start):int(end)]
