def get_clusters(M):
    attractors_idx = M.diagonal().nonzero()[0]
    clusters_idx = [M[idx].nonzero()[0] for idx in attractors_idx]
    return clusters_idx
