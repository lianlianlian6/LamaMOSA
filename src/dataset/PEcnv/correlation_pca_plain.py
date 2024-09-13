import numpy as np

def pca_plain(data, n_components=None):
    data = data.copy()
    data -= data.mean(axis=0)
    data /= data.std(axis=0)
    C = np.cov(data)
    (E, V) = np.linalg.eigh(C)
    key = np.argsort(E)[::-1][:n_components]
    (E, V) = (E[key], V[:, key])
    U = np.dot(data, V)
    return U
