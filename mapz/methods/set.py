from typing import Dict, Hashable, Any, Type

from .splitkey import splitkey, SplitkeyModificatorCallable
from .traverse import traverse, TraverseVisitorCallable
from .update import update


def set(
    mapping: Dict[Hashable, Any],
    key: Hashable,
    val: Any,
    key_prefix: str = "",
    key_sep: str = ".",
    key_modificator: SplitkeyModificatorCallable = lambda key, parts: parts,
    val_visitor: TraverseVisitorCallable = lambda k, v, **kwargs: (
        k,
        v,
    ),
    merge_method: str = "recursive",
    merge_inverse: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:

    key_parts = splitkey(
        key, prefix=key_prefix, sep=key_sep, modificator=key_modificator
    )
    value = traverse(val, val_visitor, mapping_type=mapping_type)

    # Build dict in reverse order from list of key parts and the value
    result = value
    while key_parts:
        k = key_parts.pop()
        d = mapping_type()
        dict.__setitem__(d, k, result)
        result = d

    if merge_inverse:
        update(result, mapping, method=merge_method)
        mapping.clear()

    update(mapping, result, method=merge_method)

    return mapping
