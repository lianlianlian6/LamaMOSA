import numpy as np
import pandas as pd
from pynguin.dataset.cnvkit import smoothing

def center_by_window(cnarr, fraction, sort_key):
    """Smooth out biases according to the trait specified by sort_key.

    E.g. correct GC-biased bins by windowed averaging across similar-GC
    bins; or for similar interval sizes.
    """
    df = cnarr.data.reset_index(drop=True)
    np.random.seed(679661)
    shuffle_order = np.random.permutation(df.index)
    df = df.iloc[shuffle_order]
    if isinstance(sort_key, pd.Series):
        sort_key = sort_key.values
    sort_key = sort_key[shuffle_order]
    order = np.argsort(sort_key, kind='mergesort')
    df = df.iloc[order]
    biases = smoothing.rolling_median(df['log2'], fraction)
    df['log2'] -= biases
    fixarr = cnarr.as_dataframe(df)
    fixarr.sort()
    return fixarr
