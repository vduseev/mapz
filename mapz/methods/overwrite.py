from typing import Any, Dict, Hashable, MutableMapping, Mapping


def overwrite(
    dest: Dict[Hashable, Any],
    data: Dict[Hashable, Any],
    method: str = "recursive",
) -> Dict[Hashable, Any]:

    if isinstance(dest, Dict) and isinstance(data, Mapping):

        for key in data:
            if (
                method == "recursive"
                and key in dest
                and isinstance(dict.__getitem__(dest, key), Dict)
                and isinstance(dict.__getitem__(data, key), Dict)
            ):
                overwrite(
                    dict.__getitem__(dest, key),
                    dict.__getitem__(data, key),
                    method=method,
                )

            else:
                dict.__setitem__(dest, key, dict.__getitem__(data, key))

    return dest
