from pynguin.dataset.cnvkit import plots
from pynguin.dataset.cnvkit.scatter import POINT_COLOR, get_segment_vafs, choose_segment_color, TREND_COLOR


def snv_on_genome(axis, variants, chrom_sizes, segments, do_trend, segment_color):
    """Plot a scatter-plot of SNP chromosomal positions and shifts."""
    axis.set_ylim(0.0, 1.0)
    axis.set_ylabel('VAF')
    x_starts = plots.plot_chromosome_dividers(axis, chrom_sizes)
    chrom_snvs = dict(variants.by_chromosome())
    if segments:
        chrom_segs = dict(segments.by_chromosome())
    elif do_trend:
        chrom_segs = {chrom: None for chrom in chrom_snvs}
    else:
        chrom_segs = {}
    for (chrom, x_offset) in x_starts.items():
        if chrom not in chrom_snvs:
            continue
        snvs = chrom_snvs[chrom]
        axis.scatter(snvs['start'].values + x_offset, snvs['alt_freq'].values, color=POINT_COLOR, edgecolor='none', alpha=0.2, marker='.')
        if chrom in chrom_segs:
            segs = chrom_segs[chrom]
            for (seg, v_freq) in get_segment_vafs(snvs, segs):
                if seg:
                    posn = [seg.start + x_offset, seg.end + x_offset]
                    color = choose_segment_color(seg, segment_color, default_bright=False)
                else:
                    posn = [snvs.start.iat[0] + x_offset, snvs.start.iat[-1] + x_offset]
                    color = TREND_COLOR
                axis.plot(posn, [v_freq, v_freq], color=color, linewidth=2, zorder=-1, solid_capstyle='round', snap=False)
    return axis
