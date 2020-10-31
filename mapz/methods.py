from .base import BaseMapz

from typing import (
    Any,
    Dict,
    Hashable,
    Mapping,
    MutableMapping,
    List,
    Sequence,
    Union,
    Callable,
    Tuple,
)


def set(
    self,
    key: Hashable,
    value: Any,
    method: str = "recursive",
    sep: str = ".",
    inverse: bool = False,
) -> Any:
    parsed = from_keyvalue(key, value, sep=sep)

    if inverse:
        parsed.update(self, method=method)
        self.clear()

    self.update(parsed, method=method)

    return self


def map(
    self,
    func: Callable[
        [Hashable, Any], Tuple[Hashable, Any]
    ] = lambda k, v, **kwargs: (k, v),
    inplace: bool = False,
    **kwargs,
):
    config = traverse(self, func, **kwargs)

    if inplace:
        self.clear()
        self.update(config)
        config = self

    return config


def copy(self):
    """Return deep copy of the Config object."""
    return self.map(inplace=False)


def merge(
    self,
    *mappings: Mapping[Hashable, Any],
    _method: str = "recursive",
    _sep: str = "__",
    _inverse: bool = False,
    **kwargs,
) -> BaseMapz:
    # Collect all key-value pairs from mappings and keyword arguments
    # into a single ordered list with last element having the highest
    # priority.
    items = []
    # From mappings
    for mapping in mappings:
        items += mapping.items()
    # From keyword arguments
    items += kwargs.items()

    for k, v in items:
        self.set(k, v, method=_method, sep=_sep, inverse=_inverse)

    return self


def submerge(
    self,
    *mappings: Mapping[Hashable, Any],
    _method: str = "recursive",
    _sep: str = "__",
    **kwargs,
) -> BaseMapz:
    return self.merge(
        *mappings,
        _method=_method,
        _sep=_sep,
        _inverse=True,
        **kwargs,
    )


def from_keyvalue(
    key: Hashable,
    value: Any,
    prefix: str = "",
    sep: str = "__",
    lowercase: bool = False,
    uppercase: bool = False,
) -> BaseMapz:
    parts = parse_key(
        key,
        prefix=prefix,
        sep=sep,
        lowercase=lowercase,
        uppercase=uppercase,
    )
    if not parts:
        return BaseMapz()

    # value = Config.parse_value(value)
    value = traverse(value)

    # Fill in a hierarchical structure by
    # continuously building up the config in reverse order.
    result = value
    while parts:

        # Take the last part of the key no processed yet
        k = parts.pop()

        # Create an empty config and assign current saved ``result``
        # to ``k`` in it.
        config = BaseMapz()
        dict.__setitem__(config, k, result)
        # config = Config().set(k, result)
        # config[k] = result

        # Rebind result to point to the newly created config
        result = config

    return result


def parse_key(
    key: Hashable,
    prefix: str = "",
    sep: str = "__",
    lowercase: bool = False,
    uppercase: bool = False,
) -> List[Hashable]:
    if not isinstance(key, str):
        # When key is not a string, then it cannot be split.
        # Thus, return the key as is
        return [key]

    if not isinstance(prefix, str):
        prefix = str(prefix)

    if prefix and not key.startswith(prefix):
        # If prefix is specified, then return nothing
        return []

    # Strip key off of prefix
    key = key[len(prefix) :]

    # Convert to lowercase/uppercase if needed
    key, prefix, sep = [
        v.lower() if lowercase else v.upper() if uppercase else v
        for v in [key, prefix, sep]
    ]

    # Strip any dangling separator leftovers around the key
    if sep and key.startswith(sep):
        key = key[len(sep) :]
    if sep and key.endswith(sep):
        key = key[: -len(sep)]

    # Split the key into 2 parts using the separator.
    # If the key does not contain a separator string in it, then just return a parts
    # list consisting of the key itself.
    parts = key.split(sep, maxsplit=1) if sep else [key]

    if len(parts) > 1:
        # When key has been split successfully, then the second part of the split
        # is eligible for the same processing routine and a recursive call is made.
        key, subkey = parts  # unpack split parts for readability
        return [key] + parse_key(
            subkey,
            prefix="",
            sep=sep,
            lowercase=lowercase,
            uppercase=uppercase,
        )

    else:
        # If key was not split, then there is nothing to split anymore and we just
        # return the key
        return [parts[0]]
