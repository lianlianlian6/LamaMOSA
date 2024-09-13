import os

def midsize_file(fnames):
    return sorted(fnames, key=lambda f: os.stat(f).st_size)[len(fnames) // 2 - 1]
