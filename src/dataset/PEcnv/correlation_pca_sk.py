def pca_sk(data, n_components=None):
    from sklearn.decomposition import PCA
    return PCA(n_components=n_components).fit_transform(data)
