from __future__ import division
import numpy as np

def UnifyLevels(baseLevel, addonLevel, windowSize):
    if not len(addonLevel):
        return baseLevel
    joinedLevel = []
    addon_idx = 0
    for base_elem in baseLevel:
        while addon_idx < len(addonLevel):
            addon_elem = addonLevel[addon_idx]
            if addon_elem < base_elem - windowSize:
                joinedLevel.append(addon_elem)
                addon_idx += 1
            elif base_elem - windowSize <= addon_elem <= base_elem + windowSize:
                addon_idx += 1
            else:
                assert base_elem + windowSize < addon_elem
                break
        joinedLevel.append(base_elem)
    last_pos = baseLevel[-1] + windowSize if len(baseLevel) else -1
    while addon_idx < len(addonLevel) and addonLevel[addon_idx] <= last_pos:
        addon_idx += 1
    if addon_idx < len(addonLevel):
        joinedLevel.extend(addonLevel[addon_idx:])
    return np.array(sorted(joinedLevel), dtype=np.int_)
