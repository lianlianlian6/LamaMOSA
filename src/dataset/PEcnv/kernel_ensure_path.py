import os

def ensure_path(fname):
    if '/' in os.path.normpath(fname):
        dname = os.path.dirname(os.path.abspath(fname))
        if dname and (not os.path.isdir(dname)):
            try:
                os.makedirs(dname)
            except OSError as exc:
                raise OSError('Output path ' + fname + ' contains a directory ' + dname + ' that cannot be created: %s' % exc)
    if os.path.isfile(fname):
        cnt = 1
        bak_fname = '%s.%d' % (fname, cnt)
        while os.path.isfile(bak_fname):
            cnt += 1
            bak_fname = '%s.%d' % (fname, cnt)
        os.rename(fname, bak_fname)
    return True
