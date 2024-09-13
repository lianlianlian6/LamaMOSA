import os
def rm(path):
    try:
        os.unlink(path)
    except OSError:
        pass
