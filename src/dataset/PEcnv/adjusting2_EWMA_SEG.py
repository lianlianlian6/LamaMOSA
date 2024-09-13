def EWMA_SEG(breakpoint_select):
    segs = []
    start = breakpoint_select[0]
    itm = 1
    for i in range(len(breakpoint_select)):
        if i + 1 < len(breakpoint_select):
            if itm == 1:
                start = breakpoint_select[i]
            itm += 1
            if breakpoint_select[i + 1] - breakpoint_select[i] < 20:
                if i + 1 == len(breakpoint_select) - 1:
                    if start - 20 > 0:
                        segs.append([start - 20, breakpoint_select[i + 1] + 20])
                    else:
                        segs.append([start, breakpoint_select[i + 1]])
            elif breakpoint_select[i + 1] - breakpoint_select[i] > 20:
                end = breakpoint_select[i]
                if start - 20 < 0:
                    segs.append([start, end + 20])
                else:
                    segs.append([start - 20, end + 20])
                itm = 1
    return segs
