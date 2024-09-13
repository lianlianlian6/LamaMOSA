a = 2 / 10
def adajustedEdge(index, raw_depth):
    if index <= 1:
        return raw_depth[index]
    return (1 - a) * adajustedEdge(index - 1, raw_depth) + a * raw_depth[index]
