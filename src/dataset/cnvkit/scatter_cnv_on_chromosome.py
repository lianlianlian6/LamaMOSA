import collections
import logging
import numpy as np
from pynguin.dataset.cnvkit import params
from pynguin.dataset.cnvkit.plots import MB
from pynguin.dataset.cnvkit.scatter import SEG_COLOR, set_xlim_from, setup_chromosome, highlight_genes, POINT_COLOR, \
    choose_segment_color


def cnv_on_chromosome(axis, probes, segments, genes, antitarget_marker=None, do_trend=False, x_limits=None, y_min=None, y_max=None, segment_color=SEG_COLOR):
    """Draw a scatter plot of probe values with optional segments overlaid.

    Parameters
    ----------
    genes : list
        Of tuples: (start, end, gene name)
    """
    x = 0.5 * (probes['start'] + probes['end']) * MB
    y = probes['log2']
    if 'weight' in probes:
        w = 46 * probes['weight'] ** 2 + 2
    else:
        w = np.repeat(30, len(x))
    if not y_min:
        y_min = max(-5.0, min(y.min() - 0.1, -0.3)) if len(y) else -1.1
    if not y_max:
        y_max = max(0.3, y.max() + (0.25 if genes else 0.1)) if len(y) else 1.1
    if x_limits:
        (x_min, x_max) = x_limits
        axis.set_xlim(x_min * MB, x_max * MB)
    else:
        set_xlim_from(axis, probes, segments)
    setup_chromosome(axis, y_min, y_max, 'Copy ratio (log2)')
    if genes:
        highlight_genes(axis, genes, min(2.4, y.max() + 0.1) if len(y) else 0.1)
    if antitarget_marker in (None, 'o'):
        axis.scatter(x, y, w, color=POINT_COLOR, alpha=0.4, marker='o')
    else:
        x_fg = []
        y_fg = []
        w_fg = []
        x_bg = []
        y_bg = []
        is_bg = probes['gene'].isin(params.ANTITARGET_ALIASES)
        for (x_pt, y_pt, w_pt, is_bg_pt) in zip(x, y, w, is_bg):
            if is_bg_pt:
                x_bg.append(x_pt)
                y_bg.append(y_pt)
            else:
                x_fg.append(x_pt)
                y_fg.append(y_pt)
                w_fg.append(w_pt)
        axis.scatter(x_fg, y_fg, w_fg, color=POINT_COLOR, alpha=0.4, marker='o')
        axis.scatter(x_bg, y_bg, color=POINT_COLOR, alpha=0.5, marker=antitarget_marker)
    if do_trend:
        axis.plot(x, probes.smooth_log2(), color=POINT_COLOR, linewidth=2, zorder=-1, snap=False)
    if segments:
        for row in segments:
            color = choose_segment_color(row, segment_color)
            axis.plot((row.start * MB, row.end * MB), (row.log2, row.log2), color=color, linewidth=4, solid_capstyle='round', snap=False)
        hidden_seg = segments.log2 < y_min
        if hidden_seg.sum():
            logging.warning("WARNING: With 'y_min=%s' %s segments are hidden --> Add parameter '--y-min %s' to see them", y_min, hidden_seg.sum(), int(np.floor(segments.log2.min())))
            x_hidden = segments.start[hidden_seg] * MB
            y_hidden = np.array([y_min] * len(x_hidden))
            axis.scatter(x_hidden, y_hidden, marker='^', linewidth=3, snap=False, color=segment_color, edgecolor='none', clip_on=False, zorder=10)
    return axis
