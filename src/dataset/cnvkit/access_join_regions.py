import logging
import numpy as np

def join_regions(regions, min_gap_size):
    """Filter regions, joining those separated by small gaps."""
    min_gap_size = min_gap_size or 0
    for (chrom, rows) in regions.by_chromosome():
        logging.info('%s: Joining over small gaps', chrom)
        coords = iter(zip(rows['start'], rows['end']))
        (prev_start, prev_end) = next(coords)
        for (start, end) in coords:
            gap = start - prev_end
            assert gap > 0, f'Impossible gap between {chrom} {prev_start}-{prev_end} ' + f'and {start}-{end} (={gap})'
            if gap < min_gap_size:
                logging.info('\tJoining %s %d-%d and %d-%d (gap size %d)', chrom, prev_start, prev_end, start, end, gap)
                prev_end = end
            else:
                logging.info('\tKeeping gap %s:%d-%d (size %d)', chrom, prev_end, start, gap)
                yield (chrom, prev_start, prev_end)
                (prev_start, prev_end) = (start, end)
        yield (chrom, prev_start, prev_end)
