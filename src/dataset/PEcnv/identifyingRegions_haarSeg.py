from __future__ import division
import logging
import numpy as np
import pandas as pd

from pynguin.dataset.PEcnv.identifyingRegions import HaarConv, PulseConv, FindLocalPeaks, FDRThres, UnifyLevels, \
    SegmentByPeaks


def haarSeg(I, breaksFdrQ, W=None, rawI=None, haarStartLevel=1, haarEndLevel=5):

    def med_abs_diff(diff_vals):
        """Median absolute deviation, with deviations given."""
        if len(diff_vals) == 0:
            return 0.0
        return diff_vals.abs().median() * 1.4826
    diffI = pd.Series(HaarConv(I, None, 1))
    if rawI:
        NSV_TH = 50
        varMask = rawI < NSV_TH
        pulseSize = 2
        diffMask = PulseConv(varMask, pulseSize) >= 0.5
        peakSigmaEst = med_abs_diff(diffI[~diffMask])
        noisySigmaEst = med_abs_diff(diffI[diffMask])
    else:
        peakSigmaEst = med_abs_diff(diffI)
    breakpoints = np.array([], dtype=np.int_)
    for level in range(haarStartLevel, haarEndLevel + 1):
        stepHalfSize = 2 ** level
        convRes = HaarConv(I, W, stepHalfSize)
        peakLoc = FindLocalPeaks(convRes)
        logging.debug('Found %d peaks at level %d', len(peakLoc), level)
        if rawI:
            pulseSize = 2 * stepHalfSize
            convMask = PulseConv(varMask, pulseSize) >= 0.5
            sigmaEst = (1 - convMask) * peakSigmaEst + convMask * noisySigmaEst
            convRes /= sigmaEst
            peakSigmaEst = 1.0
        T = FDRThres(convRes[peakLoc], breaksFdrQ, peakSigmaEst)
        addonPeaks = np.extract(np.abs(convRes.take(peakLoc)) >= T, peakLoc)
        breakpoints = UnifyLevels(breakpoints, addonPeaks, 2 ** (level - 1))
    logging.debug('Found %d breakpoints: %s', len(breakpoints), breakpoints)
    segs = SegmentByPeaks(I, breakpoints, W)
    segSt = np.insert(breakpoints, 0, 0)
    segEd = np.append(breakpoints, len(I))
    return {'start': segSt, 'end': segEd - 1, 'size': segEd - segSt, 'mean': segs[segSt]}
