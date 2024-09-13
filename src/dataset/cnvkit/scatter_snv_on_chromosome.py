from pynguin.dataset.cnvkit.plots import MB
from pynguin.dataset.cnvkit.scatter import POINT_COLOR, get_segment_vafs, choose_segment_color, TREND_COLOR, \
    highlight_genes


def snv_on_chromosome(axis, variants, segments, genes, do_trend, by_bin, segment_color):
    axis.set_ylim(0.0, 1.0)
    axis.set_ylabel('VAF')
    if by_bin:
        axis.set_xlabel('Position (bin)')
    else:
        axis.set_xlabel('Position (Mb)')
    axis.get_yaxis().tick_left()
    axis.get_xaxis().tick_top()
    axis.tick_params(which='both', direction='out', labelbottom=False, labeltop=False)
    x_mb = variants['start'].values * MB
    y = variants['alt_freq'].values
    axis.scatter(x_mb, y, color=POINT_COLOR, alpha=0.3)
    if segments or do_trend:
        for (seg, v_freq) in get_segment_vafs(variants, segments):
            if seg:
                posn = [seg.start * MB, seg.end * MB]
                color = choose_segment_color(seg, segment_color, default_bright=False)
            else:
                posn = [variants.start.iat[0] * MB, variants.start.iat[-1] * MB]
                color = TREND_COLOR
            axis.plot(posn, [v_freq, v_freq], color=color, linewidth=2, zorder=1, solid_capstyle='round', snap=False)
    if genes:
        highlight_genes(axis, genes, 0.9)
    return axis
