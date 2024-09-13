
import numpy as np
from pynguin.dataset.cnvkit import call

def segments2vcf(segments, ploidy, is_haploid_x_reference, diploid_parx_genome, is_sample_female):
    """Convert copy number segments to VCF records."""
    out_dframe = segments.data.reindex(columns=['chromosome', 'end', 'log2', 'probes'])
    out_dframe['start'] = segments.start.replace(0, 1)
    if 'cn' in segments:
        out_dframe['ncopies'] = segments['cn']
        abs_expect = call.absolute_expect(segments, ploidy, diploid_parx_genome, is_sample_female)
    else:
        abs_dframe = call.absolute_dataframe(segments, ploidy, 1.0, is_haploid_x_reference, diploid_parx_genome, is_sample_female)
        out_dframe['ncopies'] = abs_dframe['absolute'].round().astype('int')
        abs_expect = abs_dframe['expect']
    idx_losses = out_dframe['ncopies'] < abs_expect
    svlen = segments.end - segments.start
    svlen[idx_losses] *= -1
    out_dframe['svlen'] = svlen
    out_dframe['svtype'] = 'DUP'
    out_dframe.loc[idx_losses, 'svtype'] = 'DEL'
    out_dframe['format'] = 'GT:GQ:CN:CNQ'
    out_dframe.loc[idx_losses, 'format'] = 'GT:GQ'
    if 'ci_left' in segments and 'ci_right' in segments:
        has_ci = True
        left_margin = segments['ci_left'].values - segments.start.values
        right_margin = segments.end.values - segments['ci_right'].values
        out_dframe['ci_pos_left'] = np.r_[0, -right_margin[:-1]]
        out_dframe['ci_pos_right'] = left_margin
        out_dframe['ci_end_left'] = right_margin
        out_dframe['ci_end_right'] = np.r_[left_margin[1:], 0]
    else:
        has_ci = False
    for (out_row, abs_exp) in zip(out_dframe.itertuples(index=False), abs_expect):
        if out_row.ncopies == abs_exp or not str(out_row.probes).isdigit():
            continue
        if out_row.ncopies > abs_exp:
            genotype = f'0/1:0:{out_row.ncopies}:{out_row.probes}'
        elif out_row.ncopies < abs_exp:
            if out_row.ncopies == 0:
                gt = '1/1'
            else:
                gt = '0/1'
            genotype = f'{gt}:{out_row.probes}'
        fields = ['IMPRECISE', f'SVTYPE={out_row.svtype}', f'END={out_row.end}', f'SVLEN={out_row.svlen}', f'FOLD_CHANGE={2.0 ** out_row.log2}', f'FOLD_CHANGE_LOG={out_row.log2}', f'PROBES={out_row.probes}']
        if has_ci:
            fields.extend([f'CIPOS=({out_row.ci_pos_left},{out_row.ci_pos_right})', f'CIEND=({out_row.ci_end_left},{out_row.ci_end_right})'])
        info = ';'.join(fields)
        yield (out_row.chromosome, out_row.start, '.', 'N', f'<{out_row.svtype}>', '.', '.', info, out_row.format, genotype)
