def zip_repeater(iterable, repeatable):
    rpt_len = len(repeatable)
    if rpt_len == 1:
        rpt = repeatable[0]
        for it in iterable:
            yield (it, rpt)
    else:
        i = -1
        for (i, (it, rpt)) in enumerate(zip(iterable, repeatable)):
            yield (it, rpt)
        if i + 1 != rpt_len:
            raise ValueError('Number of unsegmented and segmented input files\n                             did not match (%d vs. %d)' % (i, rpt_len))
