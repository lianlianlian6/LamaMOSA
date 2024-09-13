def EWMA_SEG(breakpointSelects):
    segs = []
    start = breakpointSelects[0]
    itm = 1
    edgeSize = 1
    for i in range(len(breakpointSelects)):
        if i + 1 < len(breakpointSelects):
            if itm == 1:
                start = breakpointSelects[i]
            itm += 1
            if breakpointSelects[i + 1] - breakpointSelects[i] < edgeSize:
                if i + 1 == len(breakpointSelects) - 1:
                    if start - edgeSize > 0:
                        segs.append([start - edgeSize, breakpointSelects[i + 1] + edgeSize])
                    else:
                        segs.append([start, breakpointSelects[i + 1]])
            elif breakpointSelects[i + 1] - breakpointSelects[i] > edgeSize:
                end = breakpointSelects[i]
                if start - edgeSize < 0:
                    segs.append([start, end + edgeSize])
                else:
                    segs.append([start - edgeSize, end + edgeSize])
                itm = 1
    return segs
