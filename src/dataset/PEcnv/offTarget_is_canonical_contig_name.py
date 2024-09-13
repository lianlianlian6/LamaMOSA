from pynguin.dataset.PEcnv.offTarget import re_noncanonical


def is_canonical_contig_name(name):
    return not re_noncanonical.search(name)
