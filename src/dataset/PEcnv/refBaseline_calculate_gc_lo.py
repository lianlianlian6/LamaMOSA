def calculate_gc_lo(subseq):
    cnt_at_lo = subseq.count('a') + subseq.count('t')
    cnt_at_up = subseq.count('A') + subseq.count('T')
    cnt_gc_lo = subseq.count('g') + subseq.count('c')
    cnt_gc_up = subseq.count('G') + subseq.count('C')
    tot = float(cnt_gc_up + cnt_gc_lo + cnt_at_up + cnt_at_lo)
    if not tot:
        return (0.0, 0.0)
    frac_gc = (cnt_gc_lo + cnt_gc_up) / tot
    frac_lo = (cnt_at_lo + cnt_gc_lo) / tot
    return (frac_gc, frac_lo)
