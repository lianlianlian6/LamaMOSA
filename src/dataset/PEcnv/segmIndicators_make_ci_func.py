from pynguin.dataset.PEcnv.segmIndicators import confidence_interval_bootstrap


def make_ci_func(alpha, bootstraps, smoothed):

    def ci_func(ser, wt):
        return confidence_interval_bootstrap(ser, wt, alpha, bootstraps, smoothed)
    return ci_func
