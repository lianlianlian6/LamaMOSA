from pynguin.dataset.PEcnv.measures import weighted_median

def average_depth(rc_table, read_length):
    mean_depths = read_length * rc_table.mapped / rc_table.length
    return weighted_median(mean_depths, rc_table.length)
