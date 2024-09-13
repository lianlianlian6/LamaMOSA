from pynguin.dataset.cnvkit import plots
from pynguin.dataset.cnvkit.scatter import genome_scatter, chromosome_scatter, SEG_COLOR


def do_scatter(cnarr, segments=None, variants=None, show_range=None, show_gene=None, do_trend=False, by_bin=False, window_width=1000000.0, y_min=None, y_max=None, fig_size=None, antitarget_marker=None, segment_color=SEG_COLOR, title=None):
    """Plot probe log2 coverages and segmentation calls together."""
    if by_bin:
        bp_per_bin = sum((c.end.iat[-1] for (_, c) in cnarr.by_chromosome())) / len(cnarr)
        window_width /= bp_per_bin
        show_range_bins = plots.translate_region_to_bins(show_range, cnarr)
        (cnarr, segments, variants) = plots.update_binwise_positions(cnarr, segments, variants)
        global MB
        orig_mb = MB
        MB = 1
    if not show_gene and (not show_range):
        fig = genome_scatter(cnarr, segments, variants, do_trend, y_min, y_max, title, segment_color)
    else:
        if by_bin:
            show_range = show_range_bins
        fig = chromosome_scatter(cnarr, segments, variants, show_range, show_gene, antitarget_marker, do_trend, by_bin, window_width, y_min, y_max, title, segment_color)
    if by_bin:
        MB = orig_mb
    if fig_size:
        (width, height) = fig_size
        fig.set_size_inches(w=width, h=height)
    return fig
