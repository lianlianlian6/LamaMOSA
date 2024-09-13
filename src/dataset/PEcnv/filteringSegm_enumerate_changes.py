def enumerate_changes(levels):
    return levels.diff().fillna(0).abs().cumsum().astype(int)
