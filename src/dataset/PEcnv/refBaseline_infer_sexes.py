from pynguin.dataset.PEcnv.implementation import read_cna

def infer_sexes(cnn_fnames, is_haploid_x):
    sexes = {}
    for fname in cnn_fnames:
        cnarr = read_cna(fname)
        if cnarr:
            is_xx = cnarr.guess_xx(is_haploid_x)
            if is_xx is not None:
                sexes[cnarr.sample_id] = is_xx
    return sexes
