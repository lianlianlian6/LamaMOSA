from pynguin.dataset.PEcnv.implementation import read_cna

def _load_seg_dframe_id(fname):
    segarr = read_cna(fname)
    assert segarr is not None
    assert segarr.data is not None
    assert segarr.sample_id is not None
    return (segarr.data, segarr.sample_id)
