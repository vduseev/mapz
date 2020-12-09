from .traverse import traverse

from typing import Any, Dict, Hashable, Mapping, MutableMapping, Type, cast
from types import MappingProxyType


def deepclone(
    data: Mapping[Hashable, Any],
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    d = traverse(data, mapping_type=mapping_type)
    return cast(Dict[Hashable, Any], d)


def clone(
    data: Mapping[Hashable, Any],
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    d = mapping_type()

    for k in data:
        # Have to use MappingProxy as read-only alternative of dict
        # that has the same __getitem__ method.
        # That's because in case 'data' is a Mapz object its __getitem__
        # method is overwritten and has key-splitting and recursive side
        # effects.
        # To avoid invoking that we convert whatever Mapping type data is
        # into a read-only proxy and use its __getitem__ method.
        dict.__setitem__(d, k, MappingProxyType(data).__getitem__(k))
    return d
