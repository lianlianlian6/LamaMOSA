from __future__ import division

def table2coords(seg_table):
    """Return x, y arrays for plotting."""
    x = []
    y = []
    start = seg_table['start']
    size = seg_table['size']
    var = seg_table['mean']
    end = seg_table['end']
    for i in range(1, len(start)):
        for j in range(0, len(start) - i):
            if start[j] > start[j + 1]:
                (start[j], start[j + 1]) = (start[j + 1], start[j])
                (size[j], size[j + 1]) = (size[j + 1], size[j])
                (var[j], var[j + 1]) = (var[j + 1], var[j])
                (end[j], end[j + 1]) = (end[j + 1], end[j])
    for i in range(len(start)):
        x.append(start[i])
        x.append(start[i] + size[i])
        y.append(var[i])
        y.append(var[i])
    return (x, y)
