def check_unique(items, title):
    its = set(items)
    assert len(its) == 1, 'Inconsistent %s keys: %s' % (title, ' '.join(map(str, sorted(its))))
    return its.pop()
