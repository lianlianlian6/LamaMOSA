def prune(M, threshold=0.001):
    pruned = M.copy()
    pruned[pruned < threshold] = 0
    return pruned
