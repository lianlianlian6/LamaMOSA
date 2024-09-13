from __future__ import division

def breakpoint_select(dfArr, upline, dowline):
    index = 0
    breakpoints = []
    for i in dfArr:
        if i > upline or i < dowline:
            breakpoints.append(index)
        index += 1
    return breakpoints
