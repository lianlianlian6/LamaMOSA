import collections
from pynguin.dataset.PEcnv import kernel

def gene_coords_by_name(probes, names):
    names = list(filter(None, set(names)))
    if not names:
        return {}
    gene_index = collections.defaultdict(set)
    for (i, gene) in enumerate(probes['gene']):
        for gene_name in gene.split(','):
            if gene_name in names:
                gene_index[gene_name].add(i)
    all_coords = collections.defaultdict(lambda : collections.defaultdict(set))
    for name in names:
        gene_probes = probes.data.take(sorted(gene_index.get(name, [])))
        if not len(gene_probes):
            raise ValueError("No targeted gene named '%s' found" % name)
        start = gene_probes['start'].min()
        end = gene_probes['end'].max()
        chrom = kernel.check_unique(gene_probes['chromosome'], name)
        uniq_names = set()
        for oname in set(gene_probes['gene']):
            uniq_names.update(oname.split(','))
        all_coords[chrom][start, end].update(uniq_names)
    uniq_coords = {}
    for (chrom, hits) in all_coords.items():
        uniq_coords[chrom] = [(start, end, ','.join(sorted(gene_names))) for ((start, end), gene_names) in hits.items()]
    return uniq_coords
