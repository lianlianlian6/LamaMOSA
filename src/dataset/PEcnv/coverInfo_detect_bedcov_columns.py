def detect_bedcov_columns(text):
    firstline = text[:text.index('\n')]
    tabcount = firstline.count('\t')
    if tabcount < 3:
        raise RuntimeError('Bad line from bedcov:\n%r' % firstline)
    if tabcount == 3:
        return ['chromosome', 'start', 'end', 'basecount']
    if tabcount == 4:
        return ['chromosome', 'start', 'end', 'gene', 'basecount']
    fillers = ['_%d' % i for i in range(1, tabcount - 3)]
    return ['chromosome', 'start', 'end', 'gene'] + fillers + ['basecount']
