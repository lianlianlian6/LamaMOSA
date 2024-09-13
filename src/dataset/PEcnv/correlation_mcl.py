import logging

from pynguin.dataset.PEcnv.correlation import normalize, inflate, expand, converged, prune, get_clusters


def mcl(M, max_iterations, inflation, expansion=2):
    print('M_init:\n', M)
    M = normalize(M)
    for i in range(max_iterations):
        M_prev = M
        M = inflate(expand(M, expansion), inflation)
        if converged(M, M_prev):
            logging.debug('Converged at iteration %d', i)
            break
        M = prune(M)
    clusters = get_clusters(M)
    return (M, clusters)
