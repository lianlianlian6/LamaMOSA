import numpy as np

def edge_gains(target_sizes, gap_sizes, insert_size):
    """Calculate coverage gain from neighboring baits' flanking reads.

    Letting i = insert size, t = target size, g = gap to neighboring bait,
    the gain of coverage due to a nearby bait, if g < i, is::

    .. math :: (i-g)^2 / 4it

    If the neighbor flank extends beyond the target (t+g < i), reduce by::

    .. math :: (i-t-g)^2 / 4it

    If a neighbor overlaps the target, treat it as adjacent (gap size 0).
    """
    if not (gap_sizes <= insert_size).all():
        raise ValueError('Gaps greater than insert size:\n' + gap_sizes[gap_sizes > insert_size].head())
    gap_sizes = np.maximum(0, gap_sizes)
    gains = (insert_size - gap_sizes) ** 2 / (4 * insert_size * target_sizes)
    past_other_side_mask = target_sizes + gap_sizes < insert_size
    g_past = gap_sizes[past_other_side_mask]
    t_past = target_sizes[past_other_side_mask]
    gains[past_other_side_mask] -= (insert_size - t_past - g_past) ** 2 / (4 * insert_size * t_past)
    return gains
