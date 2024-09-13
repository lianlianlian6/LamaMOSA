from pynguin.dataset.PEcnv.implementation import read_cna
def merge_samples(filenames):

    def label_with_gene(cnarr):
        row2label = lambda row: '{}:{}-{}:{}'.format(row.chromosome, row.start, row.end, row.gene)
        return cnarr.data.apply(row2label, axis=1)
    if not filenames:
        return []
    first_cnarr = read_cna(filenames[0])
    out_table = first_cnarr.data.reindex(columns=['chromosome', 'start', 'end', 'gene'])
    out_table['label'] = label_with_gene(first_cnarr)
    out_table[first_cnarr.sample_id] = first_cnarr['log2']
    for fname in filenames[1:]:
        cnarr = read_cna(fname)
        if not (len(cnarr) == len(out_table) and (label_with_gene(cnarr) == out_table['label']).all()):
            raise ValueError('Mismatched row coordinates in %s' % fname)
        if cnarr.sample_id in out_table.columns:
            raise ValueError('Duplicate sample ID: %s' % cnarr.sample_id)
        out_table[cnarr.sample_id] = cnarr['log2']
        del cnarr
    return out_table
