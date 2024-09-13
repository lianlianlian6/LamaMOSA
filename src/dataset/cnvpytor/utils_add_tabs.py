from __future__ import absolute_import, print_function, division

def add_tabs(s, n=4):
    return '\n'.join(list(map(lambda x: ' ' * n + x, s.split('\n'))))
