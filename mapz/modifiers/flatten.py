"""Flatter modifier. Transforms mapping structures to flat dictionaries."""

from types import MappingProxyType
from typing import Any, Dict, Hashable, Mapping, Type, Union


def to_flat(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    prefix: str = "",
    sep: str = ".",
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Flatten mapping by concatenaiting its nested keys.

    Transforms given mapping into a flat Dict structure with no
    nested keys. Thus, there is only one level of depth in the resulting
    dictionary.

    This method was initially implemented for compatibility with
    `python-configuration`_ library. `python-configuration` uses flat
    non-nested structures internally.

    Args:
        mapping: Mapping to flatten.
        prefix (str): Optionally prepend a prefix to resulting keys. Defaults
            to empty string "".
        sep (str): Specify a separator for concatenated keys. Defaults to
            single dot ".".
        inplace (bool): If True, rebound given mapping variable to newly
            generated flattened structure. Only works if the given mapping
            is a mutable Dict. Defaults to False.
        mapping_type: Which mapping type to use to generate flattened
            structure. Defaults to ``dict``.

    Returns:
        Dict (mapping_type): Produces a dictionary of "mapping_type".

    Examples:
        Transform nested Dict structure into a flat dictionary.

        >>> m = Mapz({"this": {"is": "nested"}})
        >>> m
        MapZ{'this': MapZ{'is': 'nested'}}
        >>> to_flat(m)
        {'this.is': 'nested'}

    .. _python-configuration:
        https://github.com/tr11/python-configuration
    """

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
