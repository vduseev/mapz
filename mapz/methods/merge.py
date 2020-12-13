from .set import set as zset

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
    key_prefix: str = "",
    key_sep: str = "__",
    merge_method: str = "recursive",
    merge_inverse: bool = False,
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
            key_prefix=key_prefix,
            key_sep=key_sep,
            merge_method=merge_method,
            merge_inverse=merge_inverse,
            mapping_type=mapping_type,
        )

    return mapping
