import pandas as pd

def fmt_jtv(sample_ids, table):
    outheader = ['CloneID', 'Name'] + sample_ids
    outtable = pd.concat([pd.DataFrame({'CloneID': 'IMAGE:', 'Name': table['label']}), table.drop(['chromosome', 'start', 'end', 'gene', 'label'], axis=1)], axis=1)
    outrows = outtable.itertuples(index=False)
    return (outheader, outrows)
