
import logging

from pynguin.dataset.PEcnv.plots import update_binwise_positions_simple, update_binwise_positions


def translate_segments_to_bins(segments, bins):
    if 'probes' in segments and segments['probes'].sum() == len(bins):
        return update_binwise_positions_simple(segments)
    else:
        logging.warning("Segments %s 'probes' sum does not match the number of bins in %s", segments.sample_id, bins.sample_id)
        (_x, segments, _v) = update_binwise_positions(bins, segments)
        return segments
