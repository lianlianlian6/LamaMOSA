import collections
from pynguin.dataset.PEcnv import hyperparameters

def gene_coords_by_range(probes, chrom, start, end, ignore=hyperparameters.IGNORE_GENE_NAMES):
    """Find the chromosomal position of all genes in a range.

    Returns
    -------
    dict
        Of: {chromosome: [(start, end, gene), ...]}
    """
    ignore += hyperparameters.OFFTARGET_ALIASES
    genes = collections.OrderedDict()
    for row in probes.in_range(chrom, start, end):
        name = str(row.gene)
        if name in genes:
            genes[name][1] = row.end
        elif name not in ignore:
            genes[name] = [row.start, row.end]
    return {chrom: [(gstart, gend, name) for (name, (gstart, gend)) in list(genes.items())]}
