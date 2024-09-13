import logging
from pynguin.dataset.PEcnv import hyperparameters

def unpipe_name(name):
    if '|' not in name:
        return name
    gene_names = set(name.split('|'))
    if len(gene_names) == 1:
        return gene_names.pop()
    cleaned_names = gene_names.difference(hyperparameters.IGNORE_GENE_NAMES)
    if cleaned_names:
        gene_names = cleaned_names
    new_name = sorted(gene_names, key=len, reverse=True)[0]
    if len(gene_names) > 1:
        logging.warning('WARNING: Ambiguous gene name %r; using %r', name, new_name)
    return new_name
