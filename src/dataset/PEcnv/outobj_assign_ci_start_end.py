def assign_ci_start_end(segarr, cnarr):
    lefts_rights = ((bins.end.iat[0], bins.start.iat[-1]) for (_seg, bins) in cnarr.by_ranges(segarr, mode='outer'))
    (ci_lefts, ci_rights) = zip(*lefts_rights)
    return segarr.as_dataframe(segarr.data.assign(ci_left=ci_lefts, ci_right=ci_rights))
