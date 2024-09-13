from pynguin.dataset.PEcnv.filteringSegm import require_column, squash_by_groups


@require_column('cn')
def cn(segarr):
    return squash_by_groups(segarr, segarr['cn'])
