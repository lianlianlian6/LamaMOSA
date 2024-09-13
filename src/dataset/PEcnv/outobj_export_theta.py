import pandas as pd

from pynguin.dataset.PEcnv.outobj import ref_means_nbins, theta_read_counts


def export_theta(tumor_segs, normal_cn):
    out_columns = ['#ID', 'chrm', 'start', 'end', 'tumorCount', 'normalCount']
    if not tumor_segs:
        return pd.DataFrame(columns=out_columns)
    xy_names = []
    tumor_segs = tumor_segs.autosomes(also=xy_names)
    if normal_cn:
        normal_cn = normal_cn.autosomes(also=xy_names)
    table = tumor_segs.data.reindex(columns=['start', 'end'])
    chr2idx = {c: i + 1 for (i, c) in enumerate(tumor_segs.chromosome.drop_duplicates())}
    table['chrm'] = tumor_segs.chromosome.replace(chr2idx)
    table['#ID'] = ['start_%d_%d:end_%d_%d' % (row.chrm, row.start, row.chrm, row.end) for row in table.itertuples(index=False)]
    (ref_means, nbins) = ref_means_nbins(tumor_segs, normal_cn)
    table['tumorCount'] = theta_read_counts(tumor_segs.log2, nbins)
    table['normalCount'] = theta_read_counts(ref_means, nbins)
    return table[out_columns]
