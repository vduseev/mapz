from typing import Any, Dict, Hashable, Mapping
from types import MappingProxyType


def update(
    mapping: Dict[Hashable, Any],
    other: Mapping[Hashable, Any],
    method: str = "recursive",
) -> Dict[Hashable, Any]:

    if isinstance(mapping, Dict) and isinstance(other, Mapping):

        for key in other:
            if (
                method == "recursive"
                and key in mapping
                and isinstance(dict.__getitem__(mapping, key), Mapping)
                and isinstance(
                    MappingProxyType(other).__getitem__(key), Mapping
                )
            ):
                update(
                    dict.__getitem__(mapping, key),
                    MappingProxyType(other).__getitem__(key),
                    method=method,
                )

            else:
                dict.__setitem__(
                    mapping, key, MappingProxyType(other).__getitem__(key)
                )

    return mapping
