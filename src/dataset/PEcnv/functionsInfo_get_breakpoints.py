import math

def get_breakpoints(intervals, segments, min_probes):
    breakpoints = []
    for (i, curr_row) in enumerate(segments[:-1]):
        curr_chrom = curr_row.chromosome
        curr_end = curr_row.end
        next_row = segments[i + 1]
        if next_row.chromosome != curr_chrom:
            continue
        for (gname, gstarts, gend) in intervals[curr_chrom]:
            if gstarts[0] < curr_end < gend:
                probes_left = sum((s < curr_end for s in gstarts))
                probes_right = sum((s >= curr_end for s in gstarts))
                if probes_left >= min_probes and probes_right >= min_probes:
                    breakpoints.append((gname, curr_chrom, int(math.ceil(curr_end)), next_row.log2 - curr_row.log2, probes_left, probes_right))
    breakpoints.sort(key=lambda row: (min(row[4], row[5]), abs(row[3])), reverse=True)
    return breakpoints
