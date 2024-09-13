from pynguin.dataset.cnvkit.plots import MB
from pynguin.dataset.cnvkit.scatter import HIGHLIGHT_COLOR


def highlight_genes(axis, genes, y_posn):
    """Show gene regions with background color and a text label."""
    ngenes = len(genes)
    text_size = 'small' if ngenes <= 6 else 'x-small'
    if ngenes <= 3:
        text_rot = 'horizontal'
    elif ngenes <= 6:
        text_rot = 30
    elif ngenes <= 10:
        text_rot = 45
    elif ngenes <= 20:
        text_rot = 60
    else:
        text_rot = 'vertical'
    for gene in genes:
        (gene_start, gene_end, gene_name) = gene
        axis.axvspan(gene_start * MB, gene_end * MB, alpha=0.5, color=HIGHLIGHT_COLOR, zorder=-1)
        axis.text(0.5 * (gene_start + gene_end) * MB, y_posn, gene_name, horizontalalignment='center', rotation=text_rot, size=text_size)
