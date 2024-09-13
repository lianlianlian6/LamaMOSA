from pynguin.dataset.cnvkit.scatter import TREND_COLOR


def choose_segment_color(segment, highlight_color, default_bright=True):
    """Choose a display color based on a segment's CNA status.

    Uses the fields added by the 'call' command. If these aren't present, use
    `highlight_color` for everything.

    For sex chromosomes, some single-copy deletions or gains might not be
    highlighted, since sample sex isn't used to infer the neutral ploidies.
    """
    neutral_color = TREND_COLOR
    if 'cn' not in segment._fields:
        return highlight_color if default_bright else neutral_color
    expected_ploidies = {'chrY': (0, 1), 'Y': (0, 1), 'chrX': (1, 2), 'X': (1, 2)}
    if segment.cn not in expected_ploidies.get(segment.chromosome, [2]):
        return highlight_color
    if segment.chromosome not in expected_ploidies and 'cn1' in segment._fields and ('cn2' in segment._fields) and (segment.cn1 != segment.cn2):
        return highlight_color
    return neutral_color
