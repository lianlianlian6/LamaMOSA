def export_nexus_basic(cnarr):
    out_table = cnarr.data.reindex(columns=['chromosome', 'start', 'end', 'gene', 'log2'])
    out_table['probe'] = cnarr.labels()
    return out_table
