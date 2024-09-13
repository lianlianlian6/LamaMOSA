import collections

from pynguin.dataset.PEcnv.plots import MB


def chromosome_sizes(probes, to_mb=False):
    chrom_sizes = collections.OrderedDict()
    for (chrom, rows) in probes.by_chromosome():
        chrom_sizes[chrom] = rows['end'].max()
        if to_mb:
            chrom_sizes[chrom] *= MB
    return chrom_sizes
