from .traverse import traverse

from typing import Mapping, MutableMapping


def deepclone(data: Mapping):
    data_type = type(data)

    return traverse(data, mapping_type=data_type)


def clone(data: Mapping):
    data_type = type(data)
    d = data_type()

    for k in data:
        dict.__setitem__(d, k, dict.__getitem__(data, k))
    return d
