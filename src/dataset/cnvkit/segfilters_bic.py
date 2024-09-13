from pynguin.dataset.cnvkit.segfilters import require_column


@require_column('depth')
def bic(segarr):
    """Merge segments by Bayesian Information Criterion.

    See: BIC-seq (Xi 2011), doi:10.1073/pnas.1110574108
    """
    return NotImplemented
