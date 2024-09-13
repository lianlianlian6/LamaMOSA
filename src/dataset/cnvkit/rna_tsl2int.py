import numpy as np

def tsl2int(tsl):
    """Convert an Ensembl Transcript Support Level (TSL) code to an integer.

    The code has the format "tsl([1-5]|NA)".

    See: https://www.ensembl.org/Help/Glossary?id=492
    """
    if tsl in (np.nan, '', 'tslNA'):
        return 0
    assert tsl[:3] == 'tsl'
    value = tsl[3:]
    if len(value) > 2:
        value = value[:2].rstrip()
    if value == 'NA':
        return 0
    return int(value)
