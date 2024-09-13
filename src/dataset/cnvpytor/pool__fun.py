def _fun(f, q_in, q_out):
    while True:
        (i, x) = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))
