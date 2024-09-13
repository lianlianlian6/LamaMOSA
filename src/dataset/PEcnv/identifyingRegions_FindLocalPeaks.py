from __future__ import division
import numpy as np

def FindLocalPeaks(signal):
    maxSuspect = minSuspect = None
    peakLoc = []
    for k in range(1, len(signal) - 1):
        (sig_prev, sig_curr, sig_next) = signal[k - 1:k + 2]
        if sig_curr > 0:
            if sig_curr > sig_prev and sig_curr > sig_next:
                peakLoc.append(k)
            elif sig_curr > sig_prev and sig_curr == sig_next:
                maxSuspect = k
            elif sig_curr == sig_prev and sig_curr > sig_next:
                if maxSuspect is not None:
                    peakLoc.append(maxSuspect)
                    maxSuspect = None
            elif sig_curr == sig_prev and sig_curr < sig_next:
                maxSuspect = None
        elif sig_curr < 0:
            if sig_curr < sig_prev and sig_curr < sig_next:
                peakLoc.append(k)
            elif sig_curr < sig_prev and sig_curr == sig_next:
                minSuspect = k
            elif sig_curr == sig_prev and sig_curr < sig_next:
                if minSuspect is not None:
                    peakLoc.append(minSuspect)
                    minSuspect = None
            elif sig_curr == sig_prev and sig_curr > sig_next:
                minSuspect = None
    return np.array(peakLoc, dtype=np.int_)
