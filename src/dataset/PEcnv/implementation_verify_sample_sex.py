import logging

def verify_sample_sex(cnarr, sex_arg, is_male_reference):
    is_sample_female = cnarr.guess_xx(is_male_reference, verbose=False)
    if sex_arg:
        is_sample_female_given = sex_arg.lower() not in ['y', 'm', 'male']
        if is_sample_female != is_sample_female_given:
            logging.warning('Sample sex specified as %s but chromosomal X/Y ploidy looks like %s', 'female' if is_sample_female_given else 'male', 'female' if is_sample_female else 'male')
            is_sample_female = is_sample_female_given
    logging.info('Treating sample %s as %s', cnarr.sample_id or '', 'female' if is_sample_female else 'male')
    return is_sample_female
