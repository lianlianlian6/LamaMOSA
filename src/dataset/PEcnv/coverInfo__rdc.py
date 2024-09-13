from pynguin.dataset.PEcnv.coverInfo import _rdc_chunk


def _rdc(args):
    """Wrapper for parallel."""
    return list(_rdc_chunk(*args))
