import numpy as np

def _smooth_samples_by_weight(values, samples):
    k = len(values)
    bw = k ** (-1 / 4)
    samples = [(v + bw * np.sqrt(1 - w) * np.random.randn(k), w) for (v, w) in samples]
    return samples
