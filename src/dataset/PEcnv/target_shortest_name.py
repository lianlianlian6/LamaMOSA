from pynguin.dataset.PEcnv.target import filter_names


def shortest_name(names):
    name = min(filter_names(names), key=len)
    if len(name) > 2 and '|' in name[1:-1]:
        name = name.split('|')[-1]
    return name
