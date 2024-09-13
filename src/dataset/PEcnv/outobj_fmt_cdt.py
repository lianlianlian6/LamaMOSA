from collections import OrderedDict as OD
import pandas as pd

def fmt_cdt(sample_ids, table):
    outheader = ['GID', 'CLID', 'NAME', 'GWEIGHT'] + sample_ids
    header2 = ['AID', '', '', '']
    header2.extend(['ARRY' + str(i).zfill(3) + 'X' for i in range(len(sample_ids))])
    header3 = ['EWEIGHT', '', '', ''] + ['1'] * len(sample_ids)
    outrows = [header2, header3]
    outtable = pd.concat([pd.DataFrame.from_dict(OD([('GID', pd.Series(table.index).apply(lambda x: 'GENE%dX' % x)), ('CLID', pd.Series(table.index).apply(lambda x: 'IMAGE:%d' % x)), ('NAME', table['label']), ('GWEIGHT', 1)])), table.drop(['chromosome', 'start', 'end', 'gene', 'label'], axis=1)], axis=1)
    outrows.extend(outtable.itertuples(index=False))
    return (outheader, outrows)
