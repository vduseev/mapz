from typing import Dict, Any, Hashable, Mapping, Type, Union
from types import MappingProxyType


def to_flat(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    prefix: str = "",
    sep: str = ".",
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Flatten the mapping so that there is no hierarchy."""

    d = mapping_type()

    p = f"{prefix}" if prefix else ""
    for key in mapping:
        v = MappingProxyType(mapping).__getitem__(key)
        if isinstance(v, Mapping):
            flattened = to_flat(
                v,
                prefix=f"{p}{key}{sep}",
                sep=sep,
                mapping_type=mapping_type,
            )
            d.update(flattened)
        else:
            dict.__setitem__(d, f"{p}{key}", v)

    if isinstance(mapping, Dict) and inplace:
        mapping.clear()
        mapping.update(d)
        d = mapping

    return d
