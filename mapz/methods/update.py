"""Update method. Overwrite or merge one mapping with another."""

from enum import Enum
from types import MappingProxyType
from typing import Any, Dict, Hashable, Mapping


class Strategy(Enum):
    """Merge strategy.

    Attributes:
        Deep: Recursive merge. Instructs merge/update methods to recursively
            dive into the nested mapping objects.
        Shallow: Shallow merge. Tells merge/update methods to simply
            overwrite any duplicate keys.
    """

    Deep = 1
    Shallow = 2


def update(
    mapping: Dict[Hashable, Any],
    other: Mapping[Hashable, Any],
    strategy: Strategy = Strategy.Deep,
) -> Dict[Hashable, Any]:
    """Overwrite or merge one mapping with the other.

    This method is an extension of standard ``dict`` update method. It
    supports merge strategy on top of a simple overwrite of the fields.
    Any keys in the "other" mapping that do not exist in the original
    "mapping" are added into it. Duplicate keys in "other" overwrite
    same keys in "mapping". If merging strategy is Deep (default), then
    duplicate keys with values of Mapping type are recursively merged.

    The update strategy is controlled with the ``strategy`` enum.
    ``Strategy.Deep`` results in merging of values and ``Strategy.Shallow``
    results in fields being overwritten in the same way it happends in
    original ``dict``'s update method.

    The deep merge strategy only applies to keys with values of Mapping type.
    In such case the update will be recusrively invoked for each nested
    mapping. Otherwise, if a key contains anything other than a mapping it
    will be simply overwritten.

    This method provides the basic means of fusing two dictionaries. It has
    just a few arguments and other, more comples methods such as ``set`` and
    ``merge`` are built on top of ``update``.

    Args:
        mapping (Dict): Mutable Dict-like structure to update.
        other (Mapping): Mapping-like structure to overwrite or merge with
            the original mapping.
        strategy (Strategy): Merge strategy. ``Strategy.Deep`` causes
            recursive merge of nested mappings for duplicate keys.
            ``Strategy.Shallow`` causes overwrite of duplicate keys with
            nested mappings as values. Defaults to ``Strategy.Deep``.

    Returns:
        Dict: Original "mapping" infused with keys and values from "other".

    Examples:
        Update one mapping with the other. Notice how only "age" key gets
        updated in the original mapping because of the Deep merging strategy
        being the default merge approach in "update" method.

        >>> mapping = {"person": {"name": "Boris", "age": 36}, "job": "Cook"}
        >>> update(mapping, {"person": {"age": 37}, "job": "Programmer"})
        {'person': {'name': 'Boris', 'age': 37}, 'job': 'Programmer'}
    """

    if isinstance(mapping, Dict) and isinstance(other, Mapping):

        for key in other:
            if (
                strategy is Strategy.Deep
                and key in mapping  # noqa: W503
                and isinstance(  # noqa: W503
                    dict.__getitem__(mapping, key), Mapping
                )
                and isinstance(  # noqa: W503
                    MappingProxyType(other).__getitem__(key), Mapping
                )
            ):
                update(
                    dict.__getitem__(mapping, key),
                    MappingProxyType(other).__getitem__(key),
                    strategy=strategy,
                )

            else:
                dict.__setitem__(
                    mapping, key, MappingProxyType(other).__getitem__(key)
                )

    return mapping
