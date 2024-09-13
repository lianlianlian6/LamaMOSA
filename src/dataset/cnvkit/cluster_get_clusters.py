def get_clusters(M):
    """Extract clusters from the matrix.

    Interpretation: "Attractors" are the non-zero elements of the matrix
    diagonal. The nodes in the same row as each attractor form a cluster.

    Overlapping clusterings produced by MCL are extremely rare, and always a
    result of symmetry in the input graph.

    Returns
    -------
    result : list
        A list of arrays of sample indices. The indices in each list item
        indicate the elements of that cluster; the length of the list is the
        number of clusters.
    """
    attractors_idx = M.diagonal().nonzero()[0]
    clusters_idx = [M[idx].nonzero()[0] for idx in attractors_idx]
    return clusters_idx
