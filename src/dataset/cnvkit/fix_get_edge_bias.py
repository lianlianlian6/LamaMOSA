import numpy as np
import pandas as pd

from pynguin.dataset.cnvkit.fix import edge_losses, edge_gains


def get_edge_bias(cnarr, margin):
    """Quantify the "edge effect" of the target tile and its neighbors.

    The result is proportional to the change in the target's coverage due to
    these edge effects, i.e. the expected loss of coverage near the target
    edges and, if there are close neighboring tiles, gain of coverage due
    to "spill over" reads from the neighbor tiles.

    (This is not the actual change in coverage. This is just a tribute.)
    """
    output_by_chrom = []
    for (_chrom, subarr) in cnarr.by_chromosome():
        tile_starts = subarr['start'].values
        tile_ends = subarr['end'].values
        tgt_sizes = tile_ends - tile_starts
        losses = edge_losses(tgt_sizes, margin)
        gap_sizes = tile_starts[1:] - tile_ends[:-1]
        ok_gaps_mask = gap_sizes < margin
        ok_gaps = gap_sizes[ok_gaps_mask]
        left_gains = edge_gains(tgt_sizes[1:][ok_gaps_mask], ok_gaps, margin)
        right_gains = edge_gains(tgt_sizes[:-1][ok_gaps_mask], ok_gaps, margin)
        gains = np.zeros(len(subarr))
        gains[np.concatenate([[False], ok_gaps_mask])] += left_gains
        gains[np.concatenate([ok_gaps_mask, [False]])] += right_gains
        output_by_chrom.append(gains - losses)
    return pd.Series(np.concatenate(output_by_chrom), index=cnarr.data.index)
