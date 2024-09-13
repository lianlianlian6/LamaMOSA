from __future__ import absolute_import, print_function, division

def beta_fun(k, m, p, phased=False):
    """
    Returns likelihood beta function f(p) where 0 <= p <= 1.
    Function is not normalized.

    Parameters
    ----------
    k : int
        Number of haplotype 1 reads.
    m : int
        Number of haplotype 2 reads.
    p : float
        Parameter.
    phased : bool
        Likelihood will be symmetrised if not phased.

    Returns
    -------
    f : float
        Value od likelihood function,.

    """
    if k == m or phased:
        return 1.0 * p ** k * (1.0 - p) ** m
    else:
        return 1.0 * p ** k * (1.0 - p) ** m + 1.0 * p ** m * (1.0 - p) ** k
