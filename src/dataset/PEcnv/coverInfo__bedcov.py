from pynguin.dataset.PEcnv.coverInfo import bedcov


def _bedcov(args):
    bed_fname = args[0]
    table = bedcov(*args)
    return (bed_fname, table)
