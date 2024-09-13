import os

def midsize_file(fnames):
    """Select the median-size file from several given filenames.

    If an even number of files is given, selects the file just below the median.
    """
    assert fnames, 'No files provided to calculate the median size.'
    return sorted(fnames, key=lambda f: os.stat(f).st_size)[(len(fnames) - 1) // 2]
