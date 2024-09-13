import collections
from matplotlib import pyplot
from pynguin.dataset.cnvkit import plots
from pynguin.dataset.cnvkit.scatter import snv_on_genome, cnv_on_genome, SEG_COLOR


def genome_scatter(cnarr, segments=None, variants=None, do_trend=False, y_min=None, y_max=None, title=None, segment_color=SEG_COLOR):
    """Plot all chromosomes, concatenated on one plot."""
    if (cnarr or segments) and variants:
        axgrid = pyplot.GridSpec(5, 1, hspace=0.85)
        axis = pyplot.subplot(axgrid[:3])
        axis2 = pyplot.subplot(axgrid[3:], sharex=axis)
        axis2.tick_params(labelbottom=False)
        chrom_sizes = plots.chromosome_sizes(cnarr or segments)
        axis2 = snv_on_genome(axis2, variants, chrom_sizes, segments, do_trend, segment_color)
    else:
        (_fig, axis) = pyplot.subplots()
    if title is None:
        title = (cnarr or segments or variants).sample_id
    if cnarr or segments:
        axis.set_title(title)
        axis = cnv_on_genome(axis, cnarr, segments, do_trend, y_min, y_max, segment_color)
    else:
        axis.set_title(f'Variant allele frequencies: {title}')
        chrom_sizes = collections.OrderedDict(((chrom, subarr['end'].max()) for (chrom, subarr) in variants.by_chromosome()))
        axis = snv_on_genome(axis, variants, chrom_sizes, segments, do_trend, segment_color)
    return axis.get_figure()
