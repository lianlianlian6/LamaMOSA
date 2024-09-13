import pandas as pd

def match_ref_to_sample(ref_cnarr, samp_cnarr):
    samp_labeled = samp_cnarr.data.set_index(pd.Index(samp_cnarr.coords()))
    ref_labeled = ref_cnarr.data.set_index(pd.Index(ref_cnarr.coords()))
    for (dset, name) in ((samp_labeled, 'sample'), (ref_labeled, 'reference')):
        dupes = dset.index.duplicated()
        if dupes.any():
            raise ValueError('Duplicated genomic coordinates in ' + name + ' set:\n' + '\n'.join(map(str, dset.index[dupes])))
    ref_matched = ref_labeled.reindex(index=samp_labeled.index)
    num_missing = pd.isnull(ref_matched.start).sum()
    if num_missing > 0:
        raise ValueError('Reference is missing %d bins found in %s' % (num_missing, samp_cnarr.sample_id))
    x = ref_cnarr.as_dataframe(ref_matched.reset_index(drop=True).set_index(samp_cnarr.data.index))
    return x
