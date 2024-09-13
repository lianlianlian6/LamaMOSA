from __future__ import division

def sort_breakpoints(breakpoints):
    start = breakpoints['start']
    size = breakpoints['size']
    end = breakpoints['end']
    newBreakpoints = {}
    for i in range(1, len(start)):
        for j in range(0, len(start) - i):
            if start[j] > start[j + 1]:
                (start[j], start[j + 1]) = (start[j + 1], start[j])
                (size[j], size[j + 1]) = (size[j + 1], size[j])
                (end[j], end[j + 1]) = (end[j + 1], end[j])
    newBreakpoints['start'] = start
    newBreakpoints['end'] = end
    newBreakpoints['size'] = size
    return newBreakpoints
