import numpy as np
import pandas as pd
def _tumor_boost(t_freqs, n_freqs):
    lt_mask = t_freqs < n_freqs
    lt_idx = np.nonzero(lt_mask)[0]
    gt_idx = np.nonzero(~lt_mask)[0]
    out = pd.Series(np.zeros_like(t_freqs))
    out[lt_idx] = 0.5 * t_freqs.take(lt_idx) / n_freqs.take(lt_idx)
    out[gt_idx] = 1 - 0.5 * (1 - t_freqs.take(gt_idx)) / (1 - n_freqs.take(gt_idx))
    return out
