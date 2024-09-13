from pynguin.dataset.PEcnv.offTarget import is_canonical_contig_name, compare_chrom_names


def drop_noncanonical_contigs(preprocessible, targets, verbose=True):
    (preprocess_chroms, target_chroms) = compare_chrom_names(preprocessible, targets)
    untgt_chroms = preprocess_chroms - target_chroms
    if any((is_canonical_contig_name(c) for c in target_chroms)):
        chroms_to_skip = [c for c in untgt_chroms if not is_canonical_contig_name(c)]
    else:
        max_tgt_chr_name_len = max(map(len, target_chroms))
        chroms_to_skip = [c for c in untgt_chroms if len(c) > max_tgt_chr_name_len]
    if chroms_to_skip:
        skip_idx = preprocessible.chromosome.isin(chroms_to_skip)
        preprocessible = preprocessible[~skip_idx]
    return preprocessible
