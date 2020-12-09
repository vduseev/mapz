from typing import Dict, MutableMapping, Hashable, Any, Type

from .splitkey import splitkey, SplitkeyModificatorCallable
from .traverse import traverse, TraverseModificatorCallable
from .overwrite import overwrite


def put(
    data: Dict[Hashable, Any],
    key: Hashable,
    val: Any,
    key_prefix: str = "",
    key_sep: str = ".",
    key_modificator: SplitkeyModificatorCallable = lambda key, parts: parts,
    val_modificator: TraverseModificatorCallable = lambda k, v, **kwargs: (
        k,
        v,
    ),
    merge_method: str = "recursive",
    merge_inverse: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Any:

    key_parts = splitkey(
        key, prefix=key_prefix, sep=key_sep, modificator=key_modificator
    )
    value = traverse(val, val_modificator, mapping_type=mapping_type)

    # Build dict from list of key parts and the value
    result = value
    while key_parts:
        k = key_parts.pop()
        d = mapping_type()
        dict.__setitem__(d, k, result)
        result = d

    if merge_inverse:
        overwrite(result, data, method=merge_method)
        data.clear()

    overwrite(data, result, method=merge_method)

    return data
