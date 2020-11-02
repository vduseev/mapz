from typing import MutableMapping, Mapping


def overwrite(
    dest: MutableMapping, data: Mapping, method: str = "recursive"
) -> MutableMapping:

    if isinstance(dest, MutableMapping) and isinstance(data, Mapping):

        for key in data:
            if (
                method == "recursive"
                and key in dest
                and isinstance(dict.__getitem__(dest, key), MutableMapping)
                and isinstance(dict.__getitem__(data, key), Mapping)
            ):
                overwrite(
                    dict.__getitem__(dest, key),
                    dict.__getitem__(data, key),
                    method=method,
                )

            else:
                dict.__setitem__(dest, key, dict.__getitem__(data, key))

    return dest
