def rescale_baf(purity, observed_baf, normal_baf=0.5):
    tumor_baf = (observed_baf - normal_baf * (1 - purity)) / purity
    return tumor_baf
