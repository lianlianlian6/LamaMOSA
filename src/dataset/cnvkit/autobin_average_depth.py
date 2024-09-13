import logging
import os
import tempfile
import numpy as np
import pandas as pd
from pynguin.dataset.cnvkit import coverage, samutil
from pynguin.dataset.cnvkit.antitarget import compare_chrom_names
from pynguin.dataset.cnvkit.descriptives import weighted_median

def average_depth(rc_table, read_length):
    """Estimate the average read depth across the genome.

    Returns
    -------
    float
        Median of the per-chromosome mean read depths, weighted by chromosome
        size.
    """
    mean_depths = read_length * rc_table.mapped / rc_table.length
    return weighted_median(mean_depths, rc_table.length)