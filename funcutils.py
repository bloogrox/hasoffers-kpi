import copy
import functools
import operator


def assoc(d, k, v):
    d2 = copy.deepcopy(d)
    d2[k] = v
    return d2


def get_in(d, ks):
    return functools.reduce(operator.getitem, ks, d)


def update_in(d, ks, fn):
    d2 = copy.deepcopy(d)
    get_in(d2, ks[:-1])[ks[-1]] = fn(get_in(d2, ks))
    return d2


def assoc_in(d, ks, v):
    d2 = copy.deepcopy(d)
    get_in(d2, ks[:-1])[ks[-1]] = v
    return d2


# if __name__ == '__main__':
#     print(assoc_in([{'a': {'b': 1}}, {1:2}], [0, 'a', 'b'], 666))
