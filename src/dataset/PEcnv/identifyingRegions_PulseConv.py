from __future__ import division
import numpy as np

def PulseConv(signal, pulseSize):
    signalSize = len(signal)
    if pulseSize > signalSize:
        raise ValueError('pulseSize (%s) > signalSize (%s)' % (pulseSize, signalSize))
    pulseHeight = 1.0 / pulseSize
    result = np.zeros(signalSize, dtype=np.float_)
    for k in range((pulseSize + 1) // 2):
        result[0] += signal[k]
    for k in range(pulseSize // 2):
        result[0] += signal[k]
    result[0] *= pulseHeight
    n = 1
    for k in range(pulseSize // 2, signalSize + pulseSize // 2 - 1):
        tail = k - pulseSize
        if tail < 0:
            tail = -tail - 1
        head = k
        if head >= signalSize:
            head = signalSize - 1 - (head - signalSize)
        result[n] = result[n - 1] + (signal[head] - signal[tail]) * pulseHeight
        n += 1
    return result
