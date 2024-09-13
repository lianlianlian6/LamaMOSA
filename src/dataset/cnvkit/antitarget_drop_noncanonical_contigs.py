import logging
import re

from pynguin.dataset.cnvkit.antitarget import compare_chrom_names, is_canonical_contig_name
from pynguin.dataset.cnvkit.params import INSERT_SIZE, MIN_REF_COVERAGE, ANTITARGET_NAME

def drop_noncanonical_contigs(accessible, targets, verbose=True):
    """Drop contigs that are not targeted or canonical chromosomes.

    Antitargets will be binned over chromosomes that:

    - Appear in the sequencing-accessible regions of the reference genome
      sequence, and
    - Contain at least one targeted region, or
    - Are named like a canonical chromosome (1-22,X,Y for human)

    This allows antitarget binning to pick up canonical chromosomes that do not
    contain any targets, as well as non-canonical or oddly named chromosomes
    that were targeted.
    """
    (access_chroms, target_chroms) = compare_chrom_names(accessible, targets)
    untgt_chroms = access_chroms - target_chroms
    if any((is_canonical_contig_name(c) for c in target_chroms)):
        chroms_to_skip = [c for c in untgt_chroms if not is_canonical_contig_name(c)]
    else:
        max_tgt_chr_name_len = max(map(len, target_chroms))
        chroms_to_skip = [c for c in untgt_chroms if len(c) > max_tgt_chr_name_len]
    if chroms_to_skip:
        logging.info('Skipping untargeted chromosomes %s', ' '.join(sorted(chroms_to_skip)))
        skip_idx = accessible.chromosome.isin(chroms_to_skip)
        accessible = accessible[~skip_idx]
    return accessible
