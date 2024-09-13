import numpy as np
import pandas as pd
from pynguin.dataset.PEcnv import kernel, correct, measures, hyperparameters
from pynguin.dataset.PEcnv.implementation import read_cna
from pynguin.dataset.PEcnv.refBaseline import get_fasta_stats, bias_correct_logr


def load_sample_block(filenames, fa_fname, is_haploid_x, sexes, skip_low, correct_gc, correct_edge, correct_rmask):
    filenames = sorted(filenames, key=kernel.fbase)
    cnarr1 = read_cna(filenames[0])
    if not len(cnarr1):
        col_names = ['chromosome', 'start', 'end', 'gene', 'log2', 'depth']
        if 'gc' in cnarr1 or fa_fname:
            col_names.append('gc')
        if fa_fname:
            col_names.append('rmask')
        col_names.append('spread')
        empty_df = pd.DataFrame.from_records([], columns=col_names)
        empty_logr = np.array([[]] * (len(filenames) + 1))
        empty_dp = np.array([[]] * len(filenames))
        return (empty_df, empty_logr, empty_dp)
    ref_columns = {'chromosome': cnarr1.chromosome, 'start': cnarr1.start, 'end': cnarr1.end, 'gene': cnarr1['gene']}
    if fa_fname and (correct_rmask or correct_gc):
        (gc, rmask) = get_fasta_stats(cnarr1, fa_fname)
        if correct_gc:
            ref_columns['gc'] = gc
        if correct_rmask:
            ref_columns['rmask'] = rmask
    elif 'gc' in cnarr1 and correct_gc:
        gc = cnarr1['gc']
        ref_columns['gc'] = gc
    is_chr_x = cnarr1.chromosome == cnarr1._chr_x_label
    is_chr_y = cnarr1.chromosome == cnarr1._chr_y_label
    ref_flat_logr = cnarr1.expect_flat_log2(is_haploid_x)
    ref_edge_bias = correct.get_edge_bias(cnarr1, hyperparameters.INSERT_SIZE)
    all_depths = [cnarr1['depth'] if 'depth' in cnarr1 else np.exp2(cnarr1['log2'])]
    all_logr = [ref_flat_logr, bias_correct_logr(cnarr1, ref_columns, ref_edge_bias, ref_flat_logr, sexes, is_chr_x, is_chr_y, correct_gc, correct_edge, correct_rmask, skip_low)]
    for fname in filenames[1:]:
        cnarrx = read_cna(fname)
        if not np.array_equal(cnarr1.data.loc[:, ('chromosome', 'start', 'end', 'gene')].values, cnarrx.data.loc[:, ('chromosome', 'start', 'end', 'gene')].values):
            raise RuntimeError('%s bins do not match those in %s' % (fname, filenames[0]))
        all_depths.append(cnarrx['depth'] if 'depth' in cnarrx else np.exp2(cnarrx['log2']))
        all_logr.append(bias_correct_logr(cnarrx, ref_columns, ref_edge_bias, ref_flat_logr, sexes, is_chr_x, is_chr_y, correct_gc, correct_edge, correct_rmask, skip_low))
    all_logr = np.vstack(all_logr)
    all_depths = np.vstack(all_depths)
    ref_df = pd.DataFrame.from_dict(ref_columns)
    return (ref_df, all_logr, all_depths)
