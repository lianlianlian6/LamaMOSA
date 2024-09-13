def drop_noncanonical_contigs(region_tups):
    from .offTarget import is_canonical_contig_name
    return (tup for tup in region_tups if is_canonical_contig_name(tup[0]))
