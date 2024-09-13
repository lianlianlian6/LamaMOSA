import numpy as np
from pynguin.dataset.cnvkit import plots
from pynguin.dataset.cnvkit.scatter import POINT_COLOR, choose_segment_color, SEG_COLOR


def cnv_on_genome(axis, probes, segments, do_trend=False, y_min=None, y_max=None, segment_color=SEG_COLOR):
    """Plot bin ratios and/or segments for all chromosomes on one plot."""
    axis.axhline(color='k')
    axis.set_ylabel('Copy ratio (log2)')
    if not (y_min and y_max):
        if segments:
            low_chroms = segments.chromosome.isin(('6', 'chr6', 'Y', 'chrY'))
            seg_auto_vals = segments[~low_chroms]['log2'].dropna()
            if not y_min:
                y_min = np.nanmin([seg_auto_vals.min() - 0.2, -1.5]) if len(seg_auto_vals) else -2.5
            if not y_max:
                y_max = np.nanmax([seg_auto_vals.max() + 0.2, 1.5]) if len(seg_auto_vals) else 2.5
        else:
            if not y_min:
                y_min = -2.5
            if not y_max:
                y_max = 2.5
    axis.set_ylim(y_min, y_max)
    if probes:
        chrom_sizes = plots.chromosome_sizes(probes)
        chrom_probes = dict(probes.by_chromosome())
        window_size = int(round(0.15 * len(probes) / probes.chromosome.nunique()))
    else:
        chrom_sizes = plots.chromosome_sizes(segments)
    chrom_segs = dict(segments.by_chromosome()) if segments else {}
    x_starts = plots.plot_chromosome_dividers(axis, chrom_sizes)
    for (chrom, x_offset) in x_starts.items():
        if probes and chrom in chrom_probes:
            subprobes = chrom_probes[chrom]
            x = 0.5 * (subprobes['start'] + subprobes['end']) + x_offset
            axis.scatter(x, subprobes['log2'], marker='.', color=POINT_COLOR, edgecolor='none', alpha=0.2)
            if do_trend:
                axis.plot(x, subprobes.smooth_log2(), color=POINT_COLOR, linewidth=2, zorder=-1, snap=False)
        if chrom in chrom_segs:
            for seg in chrom_segs[chrom]:
                color = choose_segment_color(seg, segment_color)
                axis.plot((seg.start + x_offset, seg.end + x_offset), (seg.log2, seg.log2), color=color, linewidth=3, solid_capstyle='round', snap=False)
    return axis
