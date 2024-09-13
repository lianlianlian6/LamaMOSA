import pandas as pd

from pynguin.dataset.PEcnv.outobj import assign_ci_start_end, segments2vcf, VCF_HEADER


def export_vcf(segments, ploidy, is_reference_male, is_sample_female, sample_id=None, cnarr=None):
    vcf_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', sample_id or segments.sample_id]
    if cnarr:
        segments = assign_ci_start_end(segments, cnarr)
    vcf_rows = segments2vcf(segments, ploidy, is_reference_male, is_sample_female)
    table = pd.DataFrame.from_records(vcf_rows, columns=vcf_columns)
    vcf_body = table.to_csv(sep='\t', header=True, index=False, float_format='%.3g')
    return (VCF_HEADER, vcf_body)
