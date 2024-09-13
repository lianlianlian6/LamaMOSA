import numpy as np

from pynguin.dataset.PEcnv.preprocess import log_this


def get_regions(fasta_fname):
    with open(fasta_fname) as infile:
        chrom = cursor = run_start = None
        for line in infile:
            if line.startswith('>'):
                if run_start is not None:
                    yield log_this(chrom, run_start, cursor)
                chrom = line.split(None, 1)[0][1:]
                run_start = None
                cursor = 0
            else:
                line = line.rstrip()
                if 'N' in line:
                    if all((c == 'N' for c in line)):
                        if run_start is not None:
                            yield log_this(chrom, run_start, cursor)
                            run_start = None
                    else:
                        line_chars = np.array(line, dtype='c')
                        n_indices = np.where(line_chars == b'N')[0]
                        if run_start is not None:
                            yield log_this(chrom, run_start, cursor + n_indices[0])
                        elif n_indices[0] != 0:
                            yield log_this(chrom, cursor, cursor + n_indices[0])
                        gap_mask = np.diff(n_indices) > 1
                        if gap_mask.any():
                            ok_starts = n_indices[:-1][gap_mask] + 1 + cursor
                            ok_ends = n_indices[1:][gap_mask] + cursor
                            for (start, end) in zip(ok_starts, ok_ends):
                                yield log_this(chrom, start, end)
                        if n_indices[-1] + 1 < len(line_chars):
                            run_start = cursor + n_indices[-1] + 1
                        else:
                            run_start = None
                elif run_start is None:
                    run_start = cursor
                cursor += len(line)
        if run_start is not None:
            yield log_this(chrom, run_start, cursor)
