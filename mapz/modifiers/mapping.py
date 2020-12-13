from mapz.methods.traverse import traverse

from typing import Hashable, Union, Mapping, Dict, Any, cast


def to_dict(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
) -> Dict[Hashable, Any]:

    d = traverse(mapping, mapping_type=dict)

    if isinstance(mapping, Dict) and inplace:
        mapping.clear()
        mapping.update(d)
        d = mapping

    # Explicit cast here because otherwise mypy complains that 'traverse' returns Any,
    # thus 'd' also evaluates to Any, and 'to_dict' returns Dict.
    return cast(Dict[Hashable, Any], d)
