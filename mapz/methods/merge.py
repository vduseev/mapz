from .put import put

from typing import Mapping, Hashable, Any, MutableMapping


def merge(
    data: MutableMapping,
    *mappings: Mapping[Hashable, Any],
    key_prefix: str = "",
    key_sep: str = "__",
    merge_method: str = "recursive",
    merge_inverse: bool = False,
    mapping_type=dict,
) -> MutableMapping:

    # Collect all key-value pairs from mappings and keyword arguments
    # into a single ordered list with last element having the highest
    # priority.
    items = []
    # From mappings
    for mapping in mappings:
        items += mapping.items()

    for k, v in items:
        put(
            data,
            k,
            v,
            key_prefix=key_prefix,
            key_sep=key_sep,
            merge_method=merge_method,
            merge_inverse=merge_inverse,
            mapping_type=mapping_type,
        )

    return data
