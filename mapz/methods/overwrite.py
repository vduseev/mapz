from typing import Any, Dict, Hashable, MutableMapping, Mapping
from types import MappingProxyType


def overwrite(
    dest: Dict[Hashable, Any],
    data: Mapping[Hashable, Any],
    method: str = "recursive",
) -> Dict[Hashable, Any]:

    if isinstance(dest, Dict) and isinstance(data, Mapping):

        for key in data:
            if (
                method == "recursive"
                and key in dest
                and isinstance(dict.__getitem__(dest, key), Mapping)
                and isinstance(
                    MappingProxyType(data).__getitem__(key), Mapping
                )
            ):
                overwrite(
                    dict.__getitem__(dest, key),
                    MappingProxyType(data).__getitem__(key),
                    method=method,
                )

            else:
                dict.__setitem__(
                    dest, key, MappingProxyType(data).__getitem__(key)
                )

    return dest
