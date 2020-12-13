from typing import Any, Dict, Hashable, Mapping
from types import MappingProxyType

from enum import Enum


class Strategy(Enum):
    Deep = 1
    Shallow = 2


def update(
    mapping: Dict[Hashable, Any],
    other: Mapping[Hashable, Any],
    strategy: Strategy = Strategy.Deep,
) -> Dict[Hashable, Any]:

    if isinstance(mapping, Dict) and isinstance(other, Mapping):

        for key in other:
            if (
                strategy is Strategy.Deep
                and key in mapping
                and isinstance(dict.__getitem__(mapping, key), Mapping)
                and isinstance(
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
