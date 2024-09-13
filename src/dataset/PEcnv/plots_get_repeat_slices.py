import itertools
def get_repeat_slices(values):
    offset = 0
    for (idx, (_val, rpt)) in enumerate(itertools.groupby(values)):
        size = len(list(rpt))
        if size > 1:
            i = idx + offset
            slc = slice(i, i + size)
            yield (slc, size)
            offset += size - 1
