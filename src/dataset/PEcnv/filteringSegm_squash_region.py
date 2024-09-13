import numpy as np
import pandas as pd
from pynguin.dataset.PEcnv.measures import weighted_median

def squash_region(cnarr):
    assert 'weight' in cnarr
    out = {'chromosome': [cnarr['chromosome'].iat[0]], 'start': cnarr['start'].iat[0], 'end': cnarr['end'].iat[-1]}
    region_weight = cnarr['weight'].sum()
    if region_weight > 0:
        out['log2'] = np.average(cnarr['log2'], weights=cnarr['weight'])
    else:
        out['log2'] = np.mean(cnarr['log2'])
    out['gene'] = ','.join(cnarr['gene'].drop_duplicates())
    out['probes'] = cnarr['probes'].sum() if 'probes' in cnarr else len(cnarr)
    out['weight'] = region_weight
    if 'depth' in cnarr:
        if region_weight > 0:
            out['depth'] = np.average(cnarr['depth'], weights=cnarr['weight'])
        else:
            out['depth'] = np.mean(cnarr['depth'])
    if 'baf' in cnarr:
        if region_weight > 0:
            out['baf'] = np.average(cnarr['baf'], weights=cnarr['weight'])
        else:
            out['baf'] = np.mean(cnarr['baf'])
    if 'cn' in cnarr:
        if region_weight > 0:
            out['cn'] = weighted_median(cnarr['cn'], cnarr['weight'])
        else:
            out['cn'] = np.median(cnarr['cn'])
        if 'cn1' in cnarr:
            if region_weight > 0:
                out['cn1'] = weighted_median(cnarr['cn1'], cnarr['weight'])
            else:
                out['cn1'] = np.median(cnarr['cn1'])
            out['cn2'] = out['cn'] - out['cn1']
    if 'p_bintest' in cnarr:
        out['p_bintest'] = cnarr['p_bintest'].max()
    return pd.DataFrame(out)
