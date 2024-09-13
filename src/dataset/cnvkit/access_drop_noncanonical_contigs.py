import logging
import numpy as np
def drop_noncanonical_contigs(region_tups):
    """Drop contigs with noncanonical names.

    `region_tups` is an iterable of (chrom, start, end) tuples.

    Yield the same, but dropping noncanonical chrom.
    """
    from pynguin.dataset.cnvkit.antitarget import is_canonical_contig_name
    return (tup for tup in region_tups if is_canonical_contig_name(tup[0]))
