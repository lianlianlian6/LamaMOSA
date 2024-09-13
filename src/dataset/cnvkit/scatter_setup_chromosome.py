def setup_chromosome(axis, y_min=None, y_max=None, y_label=None):
    """Configure axes for plotting a single chromosome's data."""
    if y_min and y_max:
        axis.set_ylim(y_min, y_max)
        if y_min < 0 < y_max:
            axis.axhline(color='k')
    if y_label:
        axis.set_ylabel(y_label)
    axis.tick_params(which='both', direction='out')
    axis.get_xaxis().tick_bottom()
    axis.get_yaxis().tick_left()
