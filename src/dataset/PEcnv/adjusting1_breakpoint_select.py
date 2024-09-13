def breakpoint_select(dfArr, sp, upline, dowline):
    index = 0
    breakpoints = []
    for i in dfArr.ewm(span=sp).mean():
        if i > upline or i < dowline:
            breakpoints.append(index)
        index += 1
    return breakpoints
