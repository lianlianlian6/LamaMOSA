def edge_losses(target_sizes, insert_size):
    losses = insert_size / (2 * target_sizes)
    small_mask = target_sizes < insert_size
    t_small = target_sizes[small_mask]
    losses[small_mask] -= (insert_size - t_small) ** 2 / (2 * insert_size * t_small)
    return losses
