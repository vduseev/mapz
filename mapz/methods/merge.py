from .set import set as zset
from .update import Strategy

from typing import (
    Dict,
    List,
    Mapping,
    Hashable,
    Any,
    Tuple,
    Type,
)


def merge(
    mapping: Dict[Hashable, Any],
    *other: Mapping[Hashable, Any],
    prefix: str = "",
    sep: str = "__",
    strategy: Strategy = Strategy.Deep,
    inverse: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:

    # Collect all key-value pairs from mappings and keyword arguments
    # into a single ordered list with last element having the highest
    # priority.
    items: List[Tuple[Hashable, Any]] = []

    # From mappings
    for o in other:
        items += o.items()

    for k, v in items:
        zset(
            mapping,
            k,
            v,
            prefix=prefix,
            sep=sep,
            strategy=strategy,
            inverse=inverse,
            mapping_type=mapping_type,
        )

    return mapping
