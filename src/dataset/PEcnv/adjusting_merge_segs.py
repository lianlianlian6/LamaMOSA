def merge_segs(segs):
    newSegs = []
    tm = []
    for li in segs:
        if len(tm) == 0:
            tm = li
            newSegs.append(tm)
        elif li[0] <= tm[1]:
            tm = [tm[0], li[1]]
            del newSegs[-1]
            newSegs.append(tm)
        else:
            newSegs.append(li)
            tm = li
    return newSegs
