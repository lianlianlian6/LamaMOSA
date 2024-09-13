import collections
from pynguin.dataset.PEcnv import hyperparameters

def get_gene_intervals(all_probes, ignore=hyperparameters.IGNORE_GENE_NAMES):
    ignore += hyperparameters.OFFTARGET_ALIASES
    gene_probes = collections.defaultdict(lambda : collections.defaultdict(list))
    for row in all_probes:
        gname = str(row.gene)
        if gname not in ignore:
            gene_probes[row.chromosome][gname].append(row)
    intervals = collections.defaultdict(list)
    for (chrom, gp) in gene_probes.items():
        for (gene, probes) in gp.items():
            starts = sorted((row.start for row in probes))
            end = max((row.end for row in probes))
            intervals[chrom].append((gene, starts, end))
        intervals[chrom].sort(key=lambda gse: gse[1])
    return intervals
