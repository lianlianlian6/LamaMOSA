def filter_names(names, exclude=('mRNA',)):
    if len(names) > 1:
        ok_names = set((n for n in names if not any((n.startswith(ex) for ex in exclude))))
        if ok_names:
            return ok_names
    return names
