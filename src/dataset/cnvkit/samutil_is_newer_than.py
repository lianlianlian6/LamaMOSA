import os

def is_newer_than(target_fname, orig_fname):
    """Compare file modification times."""
    if not os.path.isfile(target_fname):
        return False
    return os.stat(target_fname).st_mtime >= os.stat(orig_fname).st_mtime
