import pandas as pd
def do_sex(cnarrs, is_male_refBaseline):

    def strsign(num):
        if num > 0:
            return '+%.3g' % num
        return '%.3g' % num

    def guess_and_format(cna):
        (is_xy, stats) = cna.compare_sex_chromosomes(is_male_refBaseline)
        return (cna.meta['filename'] or cna.sample_id, 'Male' if is_xy else 'Female', strsign(stats['chrx_ratio']) if stats else 'NA', strsign(stats['chry_ratio']) if stats else 'NA')
    rows = (guess_and_format(cna) for cna in cnarrs)
    columns = ['sample', 'sex', 'X_logratio', 'Y_logratio']
    return pd.DataFrame.from_records(rows, columns=columns)
