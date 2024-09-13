def filter_names(names, exclude=('mRNA',)):
    """Remove less-meaningful accessions from the given set."""
    if len(names) > 1:
        ok_names = set((n for n in names if not any((n.startswith(ex) for ex in exclude))))
        if ok_names:
            return ok_names
    return names
