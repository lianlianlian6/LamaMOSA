import logging
import numpy as np
import pandas as pd
from pynguin.dataset.PEcnv import adjusting

def center_by_window(cnarr, fraction, sort_key):
    df = cnarr.data.reset_index(drop=True)
    np.random.seed(679661)
    shuffle_order = np.random.permutation(df.index)
    df = df.iloc[shuffle_order]
    if isinstance(sort_key, pd.Series):
        sort_key = sort_key.values
    sort_key = sort_key[shuffle_order]
    order = np.argsort(sort_key, kind='mergesort')
    df = df.iloc[order]
    biases = adjusting.rolling_median(df['log2'], fraction)
    df['log2'] -= biases
    correctarr = cnarr.as_dataframe(df)
    correctarr.sort()
    return correctarr
