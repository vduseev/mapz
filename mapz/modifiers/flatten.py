from typing import Mapping


def to_flat(data: Mapping, prefix: str = "", sep: str = ".", inplace=False):
    """Flatten the mapping so that there is no hierarchy."""

    data_type = type(data)
    d = data_type()

    p = f"{prefix}" if prefix else ""
    for key in data:
        if isinstance(dict.__getitem__(data, key), Mapping):
            flattened = to_flat(dict.__getitem__(data, key), prefix=f"{p}{key}{sep}", sep=sep)
            d.update(flattened)
        else:
            dict.__setitem__(d, f"{p}{key}", dict.__getitem__(data, key))

    if inplace:
        data.clear()
        data.update(d)
        d = data

    return d
