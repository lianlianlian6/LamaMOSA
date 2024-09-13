def join_regions(regions, min_gap_size):
    min_gap_size = min_gap_size or 0
    for (chrom, rows) in regions.by_chromosome():
        coords = iter(zip(rows['start'], rows['end']))
        (prev_start, prev_end) = next(coords)
        for (start, end) in coords:
            gap = start - prev_end
            assert gap > 0, 'Impossible gap between %s %d-%d and %d-%d (=%d)' % (chrom, prev_start, prev_end, start, end, gap)
            if gap < min_gap_size:
                prev_end = end
            else:
                yield (chrom, prev_start, prev_end)
                (prev_start, prev_end) = (start, end)
        yield (chrom, prev_start, prev_end)
