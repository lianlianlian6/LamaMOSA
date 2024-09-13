def cna2df(cna):
    """Extract a subset of DataFrame columns from a CNA."""
    return cna.data.loc[:, ['start', 'end', 'log2']]
