import itertools


def flatten(ls):
    return list(itertools.chain.from_iterable(ls))
