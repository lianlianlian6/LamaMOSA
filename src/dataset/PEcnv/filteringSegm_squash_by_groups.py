import numpy as np

from pynguin.dataset.PEcnv.filteringSegm import enumerate_changes, squash_region


def squash_by_groups(cnarr, levels, by_arm=False):
    change_levels = enumerate_changes(levels)
    assert (change_levels.index == levels.index).all()
    assert cnarr.data.index.is_unique
    assert levels.index.is_unique
    assert change_levels.index.is_unique
    if by_arm:
        arm_levels = []
        for (i, (_chrom, cnarm)) in enumerate(cnarr.by_arm()):
            arm_levels.append(np.repeat(i, len(cnarm)))
        change_levels += np.concatenate(arm_levels)
    else:
        chrom_names = cnarr['chromosome'].unique()
        chrom_col = cnarr['chromosome'].replace(chrom_names, np.arange(len(chrom_names)))
        change_levels += chrom_col
    data = cnarr.data.assign(_group=change_levels)
    groupkey = ['_group']
    if 'cn1' in cnarr:
        data['_g1'] = enumerate_changes(cnarr['cn1'])
        data['_g2'] = enumerate_changes(cnarr['cn2'])
        groupkey.extend(['_g1', '_g2'])
    data = data.groupby(groupkey, as_index=False, group_keys=False, sort=False).apply(squash_region).reset_index(drop=True)
    return cnarr.as_dataframe(data)
