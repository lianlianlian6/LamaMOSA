import logging
import numpy as np

def log_this(chrom, run_start, run_end):
    """Log a coordinate range, then return it as a tuple."""
    logging.info('\tAccessible region %s:%d-%d (size %d)', chrom, run_start, run_end, run_end - run_start)
    return (chrom, run_start, run_end)
