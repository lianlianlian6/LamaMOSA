from __future__ import absolute_import, print_function, division

import logging

import numpy as np

from pynguin.dataset.cnvpytor import beta_fun

_logger = logging.getLogger("cnvpytor.utils")
def calculate_likelihood(io, bin_size, chrom, snp_use_mask=True, snp_use_id=False, snp_use_phase=False, res=200, reduce_noise=False, blw=0.8, use_hom=False):
    """
    Calculates likelihood on fly.

    Parameters
    ----------
    io : cnvpytor.IO
        IO file
    bin_size : int
        bin size
    chrom : str
        chromosome
    use_mask : bool
        Use P-mask filter if True. Default: True.
    use_id : bool
        Use id flag filter if True. Default: False.
    use_phase : bool
        Use phasing information if True and available. Default: False.
    res: int
        Likelihood function resolution. Default: 200.
    reduce_noise: bool
        Reduce noise by increasing smaller count by one. It can change final BAF level.
    blw : bool
        Exponent used in beta distribution
    use_hom : bool
        For bins without HETs estimate likelihood using number of HOMs if True.
        Use this option for calling germline deletions and CNNLOHs.


    Returns
    -------
    likelihood : numpy.array
        Likelihood array
    """
    _logger.info("Calculating likelihood for chromosome '%s'." % chrom)
    (pos, ref, alt, nref, nalt, gt, flag, qual) = io.read_snp(chrom)
    lh_x = np.linspace(0, 1, res - 1)
    max_bin = (pos[-1] - 1) // bin_size + 1
    likelihood = np.ones((max_bin, res - 1)).astype('float') / (res - 1)
    count00 = np.zeros(max_bin)
    count01 = np.zeros(max_bin)
    count10 = np.zeros(max_bin)
    count11 = np.zeros(max_bin)
    for i in range(len(pos)):
        if nalt[i] + nref[i] > 0 and (not snp_use_id or flag[i] & 1) and (not snp_use_mask or flag[i] & 2):
            if gt[i] == 1 or gt[i] == 5 or gt[i] == 6:
                b = (pos[i] - 1) // bin_size
                if snp_use_phase:
                    if gt[i] == 5:
                        count10[b] += 1
                        likelihood[b] *= beta_fun(nalt[i], nref[i], lh_x, phased=True)
                        s = np.sum(likelihood[b])
                        if s != 0.0:
                            likelihood[b] /= s
                    if gt[i] == 6:
                        count01[b] += 1
                        likelihood[b] *= beta_fun(nref[i], nalt[i], lh_x, phased=True)
                        s = np.sum(likelihood[b])
                        if s != 0.0:
                            likelihood[b] /= s
                else:
                    count01[b] += 1
                    if reduce_noise:
                        likelihood[b] *= beta_fun(nalt[i] + (1 if nalt[i] < nref[i] else 0), nref[i] + (1 if nref[i] < nalt[i] else 0), lh_x)
                    else:
                        likelihood[b] *= beta_fun(nalt[i] * blw, nref[i] * blw, lh_x)
                    s = np.sum(likelihood[b])
                    if s != 0.0:
                        likelihood[b] /= s
            else:
                b = (pos[i] - 1) // bin_size
                if snp_use_phase:
                    if gt[i] == 7:
                        count11[b] += 1
                    if gt[i] == 4:
                        count00[b] += 1
                else:
                    count11[b] += 1
    for i in range(max_bin):
        if count01[i] + count10[i] == 0 and use_hom:
            likelihood[i] = lh_x * 0.0 + 1 / res
            likelihood[i][0] = 0.5 * (count11[i] + count00[i])
            likelihood[i][-1] = 0.5 * (count11[i] + count00[i])
            s = np.sum(likelihood[i])
            likelihood[i] /= s
    return likelihood
