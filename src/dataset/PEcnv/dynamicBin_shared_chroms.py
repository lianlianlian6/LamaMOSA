def shared_chroms(*tables):
    chroms = tables[0].chromosome.drop_duplicates()
    for tab in tables[1:]:
        if tab is not None:
            new_chroms = tab.chromosome.drop_duplicates()
            chroms = chroms[chroms.isin(new_chroms)]
    return [None if tab is None else tab[tab.chromosome.isin(chroms)] for tab in tables]
