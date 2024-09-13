import functools
import logging

def require_column(*colnames):
    if len(colnames) == 1:
        msg = "'{}' filter requires column '{}'"
    else:
        msg = "'{}' filter requires columns " + ', '.join(["'{}'"] * len(colnames))

    def wrap(func):

        @functools.wraps(func)
        def wrapped_f(segarr):
            filtname = func.__name__
            if any((c not in segarr for c in colnames)):
                raise ValueError(msg.format(filtname, *colnames))
            result = func(segarr)
            logging.info("Filtered by '%s' from %d to %d rows", filtname, len(segarr), len(result))
            return result
        return wrapped_f
    return wrap
