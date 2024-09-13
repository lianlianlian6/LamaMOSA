import numpy as np

from pynguin.dataset.PEcnv.correlation import pca_sk, mcl


def markov(samples, inflation=5, max_iterations=100, by_pca=True):
    if inflation <= 1:
        raise ValueError('inflation must be > 1')
    if by_pca:
        pca_matrix = pca_sk(samples, 2)
        from scipy.spatial import distance
        dists = distance.squareform(distance.pdist(pca_matrix))
        M = 1 - dists / dists.max()
    else:
        M = np.corrcoef(samples)
    (M, clusters) = mcl(M, max_iterations, inflation)
    return clusters
