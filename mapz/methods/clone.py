from .traverse import traverse

from typing import Mapping, MutableMapping


def deepclone(data: Mapping, mapping_type=dict):
    return traverse(data, mapping_type=mapping_type)


def clone(data: Mapping, mapping_type=dict):
    d = mapping_type()

    for k in data:
        dict.__setitem__(d, k, dict.__getitem__(data, k))
    return d
