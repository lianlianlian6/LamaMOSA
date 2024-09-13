from pynguin.dataset.PEcnv.target import filter_names
from pynguin.dataset.target_shortest_name import shortest_name


def shorten_labels(gene_labels):
    longest_name_len = 0
    curr_names = set()
    curr_gene_count = 0
    for label in gene_labels:
        next_names = set(label.rstrip().split(','))
        assert len(next_names)
        overlap = curr_names.intersection(next_names)
        if overlap:
            curr_names = filter_names(overlap)
            curr_gene_count += 1
        else:
            for _i in range(curr_gene_count):
                out_name = shortest_name(curr_names)
                yield out_name
                longest_name_len = max(longest_name_len, len(out_name))
            curr_gene_count = 1
            curr_names = next_names
    for _i in range(curr_gene_count):
        out_name = shortest_name(curr_names)
        yield out_name
        longest_name_len = max(longest_name_len, len(out_name))
