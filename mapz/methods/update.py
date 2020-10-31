from mapz.base import BaseMapz


from typing import MutableMapping, Mapping

def update(
    dest: MutableMapping, data: Mapping, method: str = "recursive"
) -> BaseMapz:

    if isinstance(dest, MutableMapping) and isinstance(data, Mapping):

        for key in data:
            if (
                method == "recursive"
                and key in dest
                and isinstance(dict.__getitem__(dest, key), MutableMapping)
                and isinstance(dict.__getitem__(data, key), Mapping)
            ):
                update(
                    dict.__getitem__(dest, key),
                    dict.__getitem__(data, key),
                    method=method,
                )

            else:
                dict.__setitem__(dest, key, dict.__getitem__(data, key))

    return dest

