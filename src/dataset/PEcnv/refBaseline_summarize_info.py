import numpy as np
from pynguin.dataset.PEcnv import measures
def summarize_info(all_logr, all_depths):
    print(all_logr)
    cvg_centers = np.apply_along_axis(measures.biweight_location, 0, all_logr)
    depth_centers = np.apply_along_axis(measures.biweight_location, 0, all_depths)
    spreads = np.array([measures.biweight_midvariance(a, initial=i) for (a, i) in zip(all_logr.T, cvg_centers)])
    print(cvg_centers)
    result = {'log2': cvg_centers, 'depth': depth_centers, 'spread': spreads}
    return result
