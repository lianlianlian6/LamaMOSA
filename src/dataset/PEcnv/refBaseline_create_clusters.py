
import numpy as np

from pynguin.dataset.reference_summarize_info import summarize_info


def create_clusters(logr_matrix, min_cluster_size, sample_ids):
    from .correlation import markov, kmeans
    logr_matrix = logr_matrix[1:, :]
    print('Clustering', len(logr_matrix), 'samples...')
    clusters = kmeans(logr_matrix)
    cluster_cols = {}
    sample_ids = np.array(sample_ids)
    for (i, clust_idx) in enumerate(clusters):
        i += 1
        if len(clust_idx) < min_cluster_size:
            continue
        samples = sample_ids[clust_idx]
        clust_matrix = logr_matrix[clust_idx, :]
        clust_info = summarize_info(clust_matrix, [])
        cluster_cols.update({'log2_%d' % i: clust_info['log2'], 'spread_%d' % i: clust_info['spread']})
    return cluster_cols
