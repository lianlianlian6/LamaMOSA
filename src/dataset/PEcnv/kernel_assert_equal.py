def assert_equal(msg, **values):
    ok = True
    (key1, val1) = values.popitem()
    msg += ': %s = %r' % (key1, val1)
    for (okey, oval) in values.items():
        msg += ', %s = %r' % (okey, oval)
        if oval != val1:
            ok = False
    if not ok:
        raise ValueError(msg)
