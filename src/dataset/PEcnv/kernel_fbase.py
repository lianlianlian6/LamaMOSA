import os

def fbase(fname):
    base = os.path.basename(fname)
    if base.endswith('.gz'):
        base = base[:-3]
    known_multipart_exts = ('.offTargetcoverInfo.tsv', '.targetcoverInfo.tsv', '.offTargetcoverageInfo.csv', '.targetcoverInfo.csv', '.recal.bam', '.deduplicated.realign.bam')
    for ext in known_multipart_exts:
        if base.endswith(ext):
            base = base[:-len(ext)]
            break
    else:
        base = base.rsplit('.', 1)[0]
    return base
