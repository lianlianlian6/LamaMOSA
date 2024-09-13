def export_theta_snps(varr):
    varr = varr.autosomes(also=['chrX', 'chrY'] if varr.chromosome.iat[0].startswith('chr') else ['X', 'Y'])
    varr = varr[(varr['ref'].str.len() == 1) & (varr['alt'].str.len() == 1)]
    varr.data.dropna(subset=['depth', 'alt_count'], inplace=True)
    if 'n_depth' in varr and 'n_alt_count' in varr:
        varr.data.dropna(subset=['n_depth', 'alt_count'], inplace=True)
    varr = varr[varr['depth'] >= varr['alt_count']]
    for (depth_key, alt_key) in (('depth', 'alt_count'), ('n_depth', 'n_alt_count')):
        table = varr.data.reindex(columns=('chromosome', 'start', depth_key, alt_key))
        table = table.assign(ref_depth=table[depth_key] - table[alt_key]).reindex(columns=('chromosome', 'start', 'ref_depth', alt_key)).dropna()
        table['ref_depth'] = table['ref_depth'].astype('int')
        table[alt_key] = table[alt_key].astype('int')
        table.columns = ['#Chrm', 'Pos', 'Ref_Allele', 'Mut_Allele']
        yield table
