from typing import Dict, Any, Hashable, Mapping, Type


def to_flat(
    data: Dict[Hashable, Any],
    prefix: str = "",
    sep: str = ".",
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Flatten the mapping so that there is no hierarchy."""

    d = mapping_type()

    p = f"{prefix}" if prefix else ""
    for key in data:
        if isinstance(dict.__getitem__(data, key), Dict):
            flattened = to_flat(
                dict.__getitem__(data, key),
                prefix=f"{p}{key}{sep}",
                sep=sep,
                mapping_type=mapping_type,
            )
            d.update(flattened)
        else:
            dict.__setitem__(d, f"{p}{key}", dict.__getitem__(data, key))

    if inplace:
        data.clear()
        data.update(d)
        d = data

    return d
