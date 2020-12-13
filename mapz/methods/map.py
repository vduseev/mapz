from .traverse import traverse, TraverseVisitorCallable

from typing import Any, Dict, Hashable, Mapping, Type, Union, cast


def map(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    visitor: TraverseVisitorCallable = lambda k, v, **kwargs: (k, v),
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
    **kwargs: Any
) -> Dict[Hashable, Any]:
    d = traverse(mapping, visitor, mapping_type=mapping_type, **kwargs)

    if isinstance(mapping, Dict) and inplace:
        mapping.clear()
        mapping.update(d)
        d = mapping

    return cast(Dict[Hashable, Any], d)
