
import pandas as pd

from pynguin.dataset.cnvkit.autobin import total_region_size


def region_size_by_chrom(regions):
    chromgroups = regions.data.groupby('chromosome', sort=False)
    sizes = [total_region_size(g) for (_key, g) in chromgroups]
    return pd.DataFrame({'chromosome': regions.chromosome.drop_duplicates(), 'length': sizes})
